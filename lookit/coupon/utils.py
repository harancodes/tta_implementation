from .models import Coupon, CouponUsage
from user.models import User
from cart.models import CartAppliedCoupon
from django.utils import timezone
from decimal import Decimal
from django.db.models import Case, When, Value, CharField, F, Q

# def is_valid_coupon(code):
#     coupon = Coupon.objects.filter(code=code).first()
#     today = timezone.now().date()
#     if not coupon:
#         return False
    
#     if not coupon.is_active:
#         return False
    
#     if coupon.start_date > today or coupon.end_date < today:
#         return False
    
#     # unlimited usage
#     if coupon.usage_limit == -1:
#         return True

#     # usage limit reached
#     if coupon.usage_remaining <= 0:
#         return False
    
#     return True

def is_valid_coupon(coupon):
    """
    Returns (True, None) if coupon can be used
    Returns (False, reason) if not usable
    """
    coupon = Coupon.objects.filter(code=coupon).first()
    today = timezone.now().date()

    #invalid coupon code
    if not coupon:
        return False, "Invalid Coupon Code"

    # inactive flag
    if not coupon.is_active:
        return False, "Coupon is inactive"

    # date window check
    if coupon.start_date and coupon.start_date > today:
        return False, "Coupon not started yet"

    if coupon.end_date and coupon.end_date < today:
        return False, "Coupon expired"

    # unlimited usage
    if coupon.usage_limit == -1:
        return True, None

    # usage limit reached
    if coupon.usage_remaining <= 0:
        return False, "Coupon usage limit reached"

    return True, None




def reduce_coupon_usage_limit(code):
    coupon = Coupon.objects.filter(code=code).first()
    # -1 is for unlimited, so do nothing
    if coupon and coupon.usage_limit != -1:
        coupon.usage_remaining -= 1
        coupon.save()


def update_coupon_usage_remaining(code, new_usage_limit):
    """this function is for updaing coupon remaining usage count when updating coupons fixed usage limit."""
    coupon = Coupon.objects.get(code=code)
    new_usage_limit = int(new_usage_limit)
    
    #-1 is for unlimited
    if new_usage_limit == -1:
        coupon.usage_remaining = -1
    else:
        #we respect how much coupon already used
        coupon_used_count = CouponUsage.objects.filter(coupon=coupon).count()
        new_usage_remaining = new_usage_limit - coupon_used_count

        #usage reamining can't be negative value, so in those case set it to zero
        if new_usage_remaining > 0:
            coupon.usage_remaining = new_usage_remaining
        else:
            coupon.usage_remaining = 0
            
    coupon.save()


def create_coupon_usage_record(coupon, user):
    if coupon and user:
        CouponUsage.objects.create(coupon=coupon, user=user)
        
def coupon_eligibility_check(coupon_code, user):
    """function which return true if user never used the coupon else return false"""
    exists = CouponUsage.objects.filter(coupon__code=coupon_code, user=user)
    if exists:
        return False
    return True

def is_coupon_min_purchase_eligible(coupon_code, order_amount):
    """function which return true if users cart have the required minimum purchase amount else return false"""
    order_amount = Decimal(order_amount)
    coupon = Coupon.objects.get(code=coupon_code)
    required_min_purchase = coupon.min_purchase_amount
    if order_amount < required_min_purchase:
        return False
    return True


def clear_users_saved_coupon(coupon, user):
    """this function will remove the applied coupon from users savecoupons list and applied coupon"""
    #remove applied coupon
    CartAppliedCoupon.objects.filter(coupon=coupon, user=user).delete()
    #remove from saved coupons
    user = User.objects.get(id=user.id)
    user.saved_coupons.remove(coupon)
    
def clear_users_applied_coupon(coupon, user):
    #remove applied coupon
    CartAppliedCoupon.objects.filter(coupon=coupon, user=user).delete()
    
    
def annotate_coupon_status(coupon_set):
    """function to find and annotate coupon status to each coupon in the query set"""
    today = timezone.now().date()
    
    status_annotated_coupon_set = coupon_set.annotate(status=Case(
        When(is_active=False, then=Value('inactive')),
        When(start_date__gt=today, then=Value('upcoming')),
        When(end_date__lt=today, then=Value('expired')),
        When(Q(usage_remaining=Value(0)) & ~Q(usage_limit=Value(-1)), then=Value('maxed')),
        default=Value('active'),
        output_field=CharField()
    ))
    return status_annotated_coupon_set