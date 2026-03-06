from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import User, OTP, Address, Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .utils import (
    generate_otp,
    generate_referral_code,
    send_otp_email,
    send_email_verification,
    remove_wishlist_item,
)
from datetime import timedelta
from django.utils import timezone
from cloudinary.uploader import upload
from django.db import transaction
from django.http import JsonResponse
import json
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from django.db import transaction
from .services import validate_referral_code, give_referral_reward
from product.models import Product, Variant
from cart.models import Cart
from offer.utiils import annotate_offers
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        #check if blocked
        user_obj = User.objects.filter(email=email).first()
        if user_obj and not user_obj.is_active:
            messages.error(request, "You are blocked by admin")
            return redirect('user-login')


        user = authenticate(request, email=email, password=password)
        if user:
            # create session
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('user-login')

    # redirect authenticated users
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, "user/login.html")


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name').strip()
        referral_code = request.POST.get('referral_code').strip()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(
                request,
                "user/signup.html",
                {
                    'full_name': full_name,
                    'email': email,
                    'referral_code': referral_code,
                },
            )
        # --validate referral code and fetch details----
        referred_by = None
        if referral_code:
            user = validate_referral_code(request, referral_code)
            if not user:
                messages.error(request, "Invalid Referral Code!")
                return render(
                    request,
                    "user/signup.html",
                    {
                        'full_name': full_name,
                        'email': email,
                    },
                )
            referred_by = user.id

        request.session['signup_data'] = {
            'full_name': full_name,
            'email': email,
            'referral_code': referral_code,
            'referred_by': referred_by,
            'password': password,
        }

        return redirect('signup-send-otp')

    # redirect authenticated users
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, "user/signup.html")


def send_otp(request):
    email = request.session['signup_data'].get('email')
    otp = generate_otp()
    send_otp_email(email, otp)
    OTP.objects.create(email=email, code=otp)

    otp_resend_cooldown = timezone.now() + timedelta(minutes=settings.RESEND_OTP_AFTER)
    # Store expiry in session so it survives page reload
    request.session["otp_resend_cooldown"] = otp_resend_cooldown.timestamp()
    return redirect('signup-otp')


def otp_verification(request):
    if request.method == "POST":
        email = request.session['signup_data'].get('email')
        otp_entered = request.POST.get('otp')
        otp_record = OTP.objects.filter(email=email, code=otp_entered).last()
        raw_password = request.session['signup_data'].get('password')

        if otp_record and otp_record.is_valid():
            try:
                with transaction.atomic():
                    #--fetch referral details
                    referrer_id = request.session['signup_data'].get('referred_by')
                    referred_by = None
                    if referrer_id:
                        referred_by = User.objects.get(id=referrer_id)

                     # --finally create user-------------
                    new_user = User.objects.create_user(
                        email=request.session['signup_data'].get('email'),
                        password=raw_password,
                        full_name=request.session['signup_data'].get('full_name'),
                        referred_by=referred_by,
                        is_staff=True,
                        referral_code=generate_referral_code(),
                    )
                    new_user.save()
                    auth_user = authenticate(
                        request, email=new_user.email, password=raw_password
                    )

                    # give refferal reward if the user used referral code
                    if referred_by:
                        try:
                            give_referral_reward(new_user, referrer=referred_by)
                        except Exception as e:
                            print("Error: ", e)
                            # there is transaction.atomic() block inside give_referral_reward() method.
                            # when any exception occured inside the function the outer transaction block also need to rollback.
                            # that's why i manually raised an exception when an exception occured inside the function.
                            raise  #  forces full rollback

                    login(request, auth_user)
                    messages.success(
                        request, "Your account is all set. Start exploring now!"
                    )
                    return redirect('index')

            except Exception as e:
                print("Error on otp verification: ", e)
                messages.error(request, "Something went wrong!")
        else:
            messages.error(request, "Incorrect OTP. Please try again.")

    # redirect authenticated users
    if request.user.is_authenticated:
        return redirect('index')

    otp_resend_cooldown = request.session["otp_resend_cooldown"]
    return render(
        request, "user/otp_verification.html", {"otp_resend_cooldown": otp_resend_cooldown}
    )


def user_logout(request):
    logout(request)
    return redirect('user-login')


"""
---USER PROFILE-----------
"""


@login_required
def account_details(request):
    user = request.user
    return render(request, 'user/profile/account_details.html', {"user": user})


@login_required
def edit_profile(request):
    method = request.POST.get('_method', '').upper()

    if request.method == "POST" and method == 'PUT':
        try:
            full_name = request.POST.get('full_name').strip()
            phone = request.POST.get('phone').strip()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_image')

            dob = request.POST.get('dob')
            if dob == "":
                dob = None  # empty string in date field will raise error

            # ---upload profile pic if it exist--------------------------
            img_url = None
            image_public_id = None
            if profile_pic:
                print("undu")
                # ---upadate existing profile pic---------------------------
                if request.user.profile_img_url:
                    result = upload(
                        profile_pic,
                        folder=f"profile_images/{request.user.id}",
                        public_id=request.user.profile_img_public_id,
                        overwrite=True,
                        invalidate=True,
                        transformation=[
                            {
                                'width': 500,
                                'height': 500,
                                'crop': 'fill',  # crop to fill box, no empty space
                                'gravity': 'face',  # smart focus on detected face
                            },
                            {
                                'quality': 'auto',  # auto-tune quality
                                'fetch_format': 'auto',  # serve as webp/avif/jpg depending on browser
                            },
                        ],
                    )
                    img_url = result['secure_url']
                    image_public_id = request.user.profile_img_public_id

                # ---add profile pic for the first time---------------------
                else:
                    result = upload(
                        profile_pic,
                        folder=f"profile_images/{request.user.id}",
                        transformation=[
                            {
                                'width': 500,
                                'height': 500,
                                'crop': 'fill',
                                'gravity': 'face',
                            },
                            {
                                'quality': 'auto',
                                'fetch_format': 'auto',
                            },
                        ],
                    )
                    img_url = result['secure_url']
                    image_public_id = result['public_id']

            else:
                img_url = request.user.profile_img_url
                image_public_id = request.user.profile_img_public_id

            user = User.objects.filter(email=request.user.email).update(
                full_name=full_name,
                phone=phone,
                dob=dob,
                gender=gender,
                profile_img_url=img_url,
                profile_img_public_id=image_public_id,
            )
            messages.success(request, "PROFILE UPDATED")
            return redirect('account-details')

        # ---catch any exceptions
        except Exception as e:
            messages.error(request, e)
            return redirect('edit-profile')

    user = request.user
    return render(request, "user/profile/edit_profile.html", {"user": user})


@login_required
def profile_send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        otp = generate_otp()
        request.session["profile_email_otp"] = otp
        request.session["profile_new_email"] = email

        send_otp_email(email, otp)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
def add_address(request):
    if request.method == "POST":
        user = request.user
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        type = request.POST.get('type')


        # ---optional_fields-----------------------
        is_default = request.POST.get('is_default')
        if not is_default:
            is_default = False
        second_phone = request.POST.get('second_phone')

        try:
            Address.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                second_phone=second_phone,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode,
                type=type,
                is_default=is_default,
            )
            messages.success(request, "NEW ADDRESS ADDED")
        except Exception as e:
            print(e)
            messages.error(request, e)
        # redirect to the page where the call came from
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect('address-book')


@login_required
def edit_address(request):
    if request.method == "POST":
        user = request.user
        address_id = request.POST.get('address_id')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        address_type = request.POST.get('type')

        # ---optional_fields-----------------------
        is_default = request.POST.get('is_default')
        if not is_default:
            is_default = False
        second_phone = request.POST.get('second_phone')

        try:
            Address.objects.filter(id=address_id).update(
                user=user,
                full_name=full_name,
                phone=phone,
                second_phone=second_phone,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode,
                type=address_type,
                is_default=is_default,
            )
            # ---if it is default address set all other address is_default = false---------------
            if is_default:
                Address.objects.filter(user=user).exclude(id=address_id).update(
                    is_default=False
                )

            messages.success(request, "ADDRESS UPDATED")
        except Exception as e:
            print(e)
            messages.error(request, e)

        # redirect to the page where the call came from
        next_url = request.POST.get("next")
        if next_url:
            print(next_url)
            return redirect(next_url)
        return redirect('address-book')


@login_required
def set_default_address(request, address_id):
    try:
        Address.objects.filter(id=address_id, user=request.user).update(is_default=True)
        # set all other address is_default = false
        Address.objects.filter(user=request.user).exclude(id=address_id).update(
            is_default=False
        )
        messages.success(request, "Default Address Updated.")
    except Exception as e:
        messages.error(request, e)
    return redirect('address-book')


@login_required
def delete_address(request):
    request_from = None
    if request.method == "POST":
        address_id = request.POST.get('address_id')
        request_from = request.POST.get('request_from')
        try:
            with transaction.atomic():
                address = Address.objects.get(id=address_id)
                address.is_active = False

                # if default address set new one
                if address.is_default:
                    latest_address = (
                        Address.objects.exclude(id=address.id)
                        .filter(is_active=True)
                        .order_by('-created_at')
                        .first()
                    )
                    if latest_address:
                        latest_address.is_default = True
                        latest_address.save()
                address.is_default = False
                address.save()
                messages.success(request, "ADDRESS DELETED")
        except Exception as e:
            messages.error(request, e)

    if request_from == 'address_book':
        return redirect('address-book')
    return redirect('checkout')


@login_required
@require_POST
def change_password(request):
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    email = request.user.email
    user = request.user

    auth_user = authenticate(email=email, password=current_password)
    if auth_user:
        try:
            with transaction.atomic():
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "PASSWORD CHANGED SUCCESSFULLY")
        except Exception as e:
            messages.error(request, e)
    else:
        messages.error(request, "INVALID PASSWORD")
    return redirect('account-details')


@login_required
def address_book(request):
    address_list = Address.objects.filter(user=request.user, is_active=True).order_by(
        "-is_default", "-created_at"
    )
    return render(
        request, "user/profile/address_book.html", {"address_list": address_list}
    )


"""
---EMAIL VERIFICATION-------------------------------
"""


@login_required
def change_user_email(request):
    print("call is here.....")
    data = json.loads(request.body)
    new_email = data.get('email')

    # check if it already exist
    email_exist = User.objects.filter(email=new_email).exists()
    if email_exist:
        # error response - will reload page using js
        messages.error(request, "Email already exist")
        return JsonResponse({'error_redirect_url': reverse('edit-profile')})

    # Store temporarily
    request.session['pending_new_email'] = new_email

    # Send verification mail
    send_email_verification(request.user, new_email, request)

    # success response - will reload page using js
    messages.success(request, "Verification Link Sent")
    return JsonResponse(
        {
            'message': 'Verification email sent!',
            'success_redirect_url': reverse('edit-profile'),
        }
    )


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    new_email = request.GET.get('new_email')

    if user and default_token_generator.check_token(user, token):
        # check if session active
        if not request.user.is_authenticated:
            messages.error(request, "Session Expired! Please Try Again.")
            return redirect("account-details")  # redirect to profile page
        user.email = new_email
        user.pending_email = None
        user.save()
        messages.success(request, "Email updated successfully!")
    else:
        messages.error(request, "Invalid or expired verification link.")

    return redirect("account-details")  # redirect to profile page


@login_required
def wishlist(request):
    wishlist_products = None
    try:
        items = (
            Wishlist.objects.filter(user=request.user, product__variant__stock__gt=0)
            .prefetch_related('product__variant')
            .distinct()
        )
        
        # Get the product queryset instead of wishlist items for annotating offers
        products_qs = Product.objects.filter(id__in=items.values_list('product_id', flat=True))
        # annotate offer price to each product
        wishlist_products = annotate_offers(products_qs)

    except Exception as e:
        print("Error while loading wishlist: ", e)
        messages.error(request, "Something went wrong!")
        return redirect('explore')

    return render(request, "user/profile/wishlist.html", {"wishlist_products": wishlist_products})


@login_required
def add_to_wishlist(request):
    if request.method == "POST":
        user = request.user
        product_uuid = request.POST.get('product_uuid')

        try:
            product = Product.objects.filter(uuid=product_uuid).first()

            # invalid uuid
            if not product:
                print("product uuid is invalid or null, uuid = ", product_uuid)
                messages.error(request, "Something went wrong!")
                return redirect('explore')

            already_exist = Wishlist.objects.filter(
                user=request.user, product=product
            ).exists()
            if already_exist:
                messages.error(request, "Product already exist in wishlist!")
                return redirect('product-details', product_uuid=product_uuid)

            Wishlist.objects.create(user=user, product=product)
            messages.success(request, "Product added to wishlist")
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong!")

        return redirect('product-details', product_uuid=product_uuid)


@require_POST
@login_required
def toggle_wishlist_ajax(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    try:
        wishlist_exists = Wishlist.objects.filter(
            user=request.user, product_id=product_id
        ).exists()
        if wishlist_exists:
            Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
            return JsonResponse({"status": "removed"})
        else:
            product = Product.objects.get(id=product_id)
            Wishlist.objects.create(user=request.user, product=product)
            return JsonResponse({"status": "added"})
    except Exception as e:
        print("Error: ", e)
        return JsonResponse({"status": "failed"})


@login_required
def remove_from_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        try:
            remove_wishlist_item(request.user, product_id)
            messages.success(request, "Item removed from wishlist")
        except Exception as e:
            print("Error on remove from wishlist: ", e)
            messages.error(request, "Something went wrong!")

    return redirect('wishlist')


@login_required
def wishilst_move_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        variant_id = request.POST.get("variant_id")
        print(variant_id)
        print(product_id)
        try:
            with transaction.atomic():

                product = Product.objects.get(id=product_id)
                user = request.user

                # if size not selected
                if not variant_id:
                    messages.error(request, "Please select a size")
                    return redirect("wishlist")

                # check if product is active
                if not product.is_active:
                    messages.error(request, "Product Is Currently Unavailble")
                    return redirect('wishlist')

                # --stock validation---
                variant = Variant.objects.get(id=variant_id)
                if int(variant.stock) == 0:
                    messages.error(
                        request,
                        f"{variant.product.name} ( Size-{variant.size} ) Is Currently Out Of Stock.",
                    )
                    return redirect("wishlist")

                # check if variant already exist
                already_exist = Cart.objects.filter(user=user, variant=variant).exists()
                if already_exist:
                    messages.error(
                        request, f"Product with size {variant.size} is already in cart"
                    )
                    return redirect('wishlist')

                Cart.objects.create(user=user, variant_id=variant_id, quantity=1)
                remove_wishlist_item(request.user, product_id)
                messages.success(request, "Item Moved to Cart")

        except Exception as e:
            print("Error on move to cart from wishlist: ", e)
            messages.error(request, "Something went wrong!")

    return redirect('wishlist')


@login_required
def clear_wishlist(request):
    try:
        Wishlist.objects.filter(user=request.user).delete()
        messages.success(request, "Wishlist cleared")
    except Exception as e:
        print("Error while clearing wishlist: ", e)
        messages.error(request, "Something went wrong!")

    return redirect('wishlist')
