from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import razorpay
from .models import Payment
from order.models import Order, OrderItems
from cart.models import Cart
from wallet.models import Wallet, WalletTransactions
from order.utils import reduce_stock_for_order, check_stock_and_availability_for_order
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from coupon.utils import reduce_coupon_usage_limit, create_coupon_usage_record, clear_users_saved_coupon
import json
from cart.utils import calculate_cart_summary



# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def create_razorpay_order(request):
    
    # --cart is empty validation------------------------------
    cart_count = Cart.objects.filter(user=request.user).count()
    if cart_count == 0:
        return JsonResponse({'failed':True})
    
    data = json.loads(request.body)
    order_id = data.get('order_id')
    order = None
    try:
        order = Order.objects.get(id=order_id)
        
        #check if stock still available before opening razorpay modal
        check_stock_and_availability_for_order(order)
        
        summary = calculate_cart_summary(request.user)
        cart_summary = summary.get('cart_summary')
        amount_in_rs = cart_summary.get('grand_total')

        amount = int(amount_in_rs * 100)    # Rs. 200 in paise
        currency = 'INR'

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(
            dict(amount=amount, currency=currency, payment_capture='0')
        )
        
        # Save order in database
        Payment.objects.create(
            user = request.user,
            order = order,
            razorpay_order_id=razorpay_order['id'],
            amount=amount,
            status='Created'
        )

        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': reverse('razorpay_paymenthandler'),
            'name':'LookIt'
        }
        
        return JsonResponse(context)
    except Exception as e:
        print("Error while opening razorpay model: ", e)
        return JsonResponse({'failed':True})

@csrf_exempt
@login_required
def paymenthandler(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")
    
    payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        # Verify payment signature
        razorpay_client.utility.verify_payment_signature(params_dict)
        with transaction.atomic():
            
            payment = Payment.objects.select_for_update().get(razorpay_order_id=razorpay_order_id)

            # Idempotency guard
            if payment.status == "Success":
                return redirect("order-success", order_uuid=payment.order.uuid)

            # Capture payment
            razorpay_client.payment.capture(payment_id, payment.amount)

            # Update payment record
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()
            
            #fetch related order and update payment status
            order = Order.objects.select_for_update().get(id=payment.order_id)
            order.payment_method = Order.PaymentMethod.ONLINE_PAYMENT
            order.items.update(order_status = OrderItems.OrderStatus.PLACED, payment_status = OrderItems.PaymentStatus.PAID, placed_at=timezone.now())
            order.save()
            
            # --handle stock count of the product---
            reduce_stock_for_order(order.id)
            
            #--reduce coupon usage limit if applied any------
            order = Order.objects.select_for_update().get(id=order.id)
            if order.coupon_applied:
                reduce_coupon_usage_limit(order.coupon_applied.code)
                create_coupon_usage_record(order.coupon_applied, request.user)
                clear_users_saved_coupon(order.coupon_applied, request.user)

            return redirect('order-success', order_uuid=order.uuid)

    except razorpay.errors.SignatureVerificationError:
        # Update payment as failed
        Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(status='Failed')
        return redirect('payment-failed', order_uuid=order.uuid)

    except Exception as e:
        print("Error: ",e)
        messages.error(request, "Something went wrong")
        return redirect('payment-failed', order_uuid=order.uuid)


    
    
#RAZORPAY FOR WALLET TOPUP
@login_required
def create_razorpay_wallet_topup(request):
    data = json.loads(request.body)
    amount_to_pay = data.get('amount')
    
    amount = amount_to_pay * 100  # convert to paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture='0')
    )
    
    # Save order in database
    Payment.objects.create(
        user = request.user,
        razorpay_order_id=razorpay_order['id'],
        amount=amount,
        status='Created'
    )

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': reverse('wallet-topup-payment-handler'),
        'failure_url': reverse('wallet'),
        'name':'LookIt'
    }
    
    return JsonResponse(context)



@csrf_exempt
@login_required
def wallet_topup_paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Capture payment
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            razorpay_client.payment.capture(payment_id, payment.amount)

            # Update payment record
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()
            
            
            #convert amount in paise to rupees
            amount_in_paise = payment.amount
            amount_in_rupees = amount_in_paise / 100
            print(amount_in_rupees)
            
            #create a wallet transaction
            try:
                with transaction.atomic():
                    wallet = Wallet.objects.get(user=request.user)
                    WalletTransactions.objects.create(
                        wallet=wallet,
                        amount = amount_in_rupees,
                        transaction_type = WalletTransactions.TransactionType.CREDIT,
                        label = "Topup to Wallet",
                        txn_source = WalletTransactions.TransactionSource.ONLINE,
                    )
                    wallet.balance += Decimal(amount_in_rupees)
                    wallet.save()
                    messages.success(request, f"Wallet toput of amount {amount_in_rupees} is success")
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                
            return redirect('wallet')
        
        except razorpay.errors.SignatureVerificationError:
            # Update payment as failed
            print("failed")
            Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(status='Failed')
            return redirect('wallet')
        
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return HttpResponseBadRequest("Invalid request method")