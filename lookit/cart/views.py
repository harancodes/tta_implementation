from django.shortcuts import render, redirect
from .models import Cart, CartAppliedCoupon
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db import transaction
from product.models import Variant
from coupon.utils import is_valid_coupon, coupon_eligibility_check, is_coupon_min_purchase_eligible
from coupon.models import Coupon
from .utils import calculate_cart_summary
from django.conf import settings

@login_required
def cart(request):
    summary = calculate_cart_summary(request.user)
    cart_items = summary.get('items')
    cart_summary = summary.get('cart_summary')
    applied_coupon = summary.get('applied_coupon')
    
    # --for disabling checkout button if a product is unavailable or out of stock
    checkout_block = False
    for item in cart_items:
        if not item.stock_available or not item.is_product_active:
            checkout_block = True
            break

    # --fetch all saved coupons by user
    user = request.user
    saved_coupons = user.saved_coupons.all()

    return render(
        request,
        'cart/cart.html',
        {
            "cart_items": cart_items,
            "cart_summary": cart_summary,
            "checkout_block": checkout_block,
            "saved_coupons": saved_coupons,
            "applied_coupon": applied_coupon,
            "max_quantity": settings.MAX_CART_QUANTITY
        },
    )


@login_required
def remove_cart_item(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        try:
            Cart.objects.filter(variant_id=variant_id).delete()
            messages.success(request, "ITEM REMOVED FROM CART")
        except Exception as e:
            messages.error(request, e)

    return redirect('cart')


@login_required
def update_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)

        cart_id = data.get('cart_id')
        variant_id = data.get('variant_id')
        new_quantity = data.get('new_quantity')

        try:
            with transaction.atomic():
                cart_item = Cart.objects.get(id=cart_id, variant_id=variant_id)
                product_variant = Variant.objects.get(id=variant_id)

                old_quantity = cart_item.quantity
                cart_item.quantity = new_quantity
                quantity_change = new_quantity - old_quantity

                if quantity_change > 0:
                    if product_variant.stock < new_quantity:
                        return JsonResponse(
                            {
                                "error": "Stock not available",
                                "quantity": old_quantity,
                            }
                        )

                product_variant.save()
                cart_item.save()
        except Exception as e:
            print("ERROR: ", e)
            messages.error(request, "Something went wrong!")

    # ---fetch updated cart summary----
    cart_record = calculate_cart_summary(request.user)
    cart_items = cart_record['items']
    cart_items = (
        cart_items
        .annotate(
            unit_price=F('variant__product__price'),
        )
    )
    # cart price summary
    cart_summary = cart_record['cart_summary']

    cart_items = list(
        cart_items.values('id', 'quantity', 'unit_price', 'sub_total')
    )

    return JsonResponse(
        {
            "status": "success",
            "message": "Quantity updated",
            "new_quantity": new_quantity,
            "cart_summary": cart_summary,
            "cart_items": cart_items,
        }
    )


@login_required
def save_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        # --check validity-------------------------
        valid_coupon, reason = is_valid_coupon(coupon_code)
        
        # --check if user already used the coupon
        eligible = coupon_eligibility_check(coupon_code, request.user)
        if not eligible:
            messages.error(request, "You can only use a coupon once!")
            return redirect('cart')

        if valid_coupon:
            coupon = Coupon.objects.get(code=coupon_code)
            request.user.saved_coupons.add(coupon)
            messages.success(request, 'New Coupon Saved Successfully')
        else:
            messages.error(request, reason)

    return redirect('cart')


@login_required
def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        cart_amount = request.POST.get('cart-total')

        # --check if user already applied another coupon
        applied_coupon_exist = CartAppliedCoupon.objects.filter(
            user=request.user
        ).exists()
        if applied_coupon_exist:
            messages.error(request, "Only one coupon can be applied at a time")
            return redirect('cart')

        # --check validity-------------------------
        valid_coupon, reason = is_valid_coupon(coupon_code)
        
        # --check if user already used the coupon
        eligible = coupon_eligibility_check(coupon_code, request.user)

        # --check if users cart have min purchase amount required for coupon
        coupon_meets_min_purchase = is_coupon_min_purchase_eligible(coupon_code, cart_amount)
        
        if not eligible:
            messages.error(request, "You can only use a coupon once!")
            return redirect('cart')
        
        if not coupon_meets_min_purchase:
            coupon = Coupon.objects.get(code=coupon_code)
            messages.error(request,f"This coupon requires a minimum purchase of ₹{coupon.min_purchase_amount}.")
            return redirect('cart')

        if valid_coupon:
            coupon = Coupon.objects.get(code=coupon_code)

            # --add coupon to users cart-------------------
            try:
                CartAppliedCoupon.objects.create(user=request.user, coupon=coupon)
                messages.success(request, 'Coupon Applied Successfully')
            except Exception as e:
                print("Error: ", e)
                messages.error(request, "Something went wrong!")

        else:
            messages.error(request, reason)

    return redirect('cart')


@login_required
def remove_coupon(request):
    if request.method == 'POST':
        # --remove applied coupon of the user-----------------------
        try:
            CartAppliedCoupon.objects.filter(user=request.user).delete()
            messages.success(request, "Applied coupon removed")
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong!")

        return redirect('cart')
