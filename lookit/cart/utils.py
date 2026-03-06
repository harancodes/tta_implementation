# cart/utils.py
from offer.models import Offer
from django.db.models import (
    ExpressionWrapper,
    DecimalField,
    F,
    Value,
    IntegerField,
    OuterRef,
    Subquery,
    Max,
    Case,
    When,
    BooleanField,
    Sum,
)
from cart.models import Cart, CartAppliedCoupon
from offer.models import Offer
from django.db.models.functions import Coalesce, Greatest, Round
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone


def calculate_cart_summary(user):
    """
    Centralized cart total calculator.
    Handles product discounts, coupon discounts, and returns a summary dict.
    """
    # sub queries for fetching offers
    today = timezone.now().date()
    product_discount_sq = (
        Offer.objects.filter(
            products=OuterRef('variant__product__id'),
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .values('products')
        .annotate(max_discount=Max('discount'))
        .values('max_discount')[:1]
    )

    category_discount_sq = (
        Offer.objects.filter(
            style=OuterRef('variant__product__style'),
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .values('style')
        .annotate(max_discount=Max('discount'))
        .values('max_discount')[:1]
    )

    # ---products in order------------------------------------------------
    cart_items = (
        Cart.objects.filter(user=user)
        .select_related('variant')
        .annotate(
            sub_total_per_product=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            stock_available=Case(
                When(variant__stock__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            available_stock_count=F('variant__stock'),
            is_product_active=F('variant__product__is_active'),
        )
        .order_by('-stock_available', '-is_product_active')
        # fetch product discount and offer discount percentage for calculation
        .annotate(
            product_discount=Coalesce(
                Subquery(product_discount_sq), Value(0), output_field=IntegerField()
            ),
            category_discount=Coalesce(
                Subquery(category_discount_sq), Value(0), output_field=IntegerField()
            ),
        )
        # take biggest discount from product or category
        .annotate(
            offer_percentage=Greatest(F('product_discount'), F('category_discount'))
        )
        # discount amount per item
        .annotate(
            discount_amount=ExpressionWrapper(
                Round(
                    (F('variant__product__price') * F('offer_percentage') / Value(100)),
                    2,
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        # total discount applied considering quantity
        .annotate(
            discount_subtotal=ExpressionWrapper(
                (F('discount_amount') * F('quantity')),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        # price of item considering offer
        .annotate(
            offer_price=ExpressionWrapper(
                (F('variant__product__price') - F('discount_amount')),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        # price of product considering quantity
        .annotate(
            sub_total=ExpressionWrapper(
                (F('offer_price') * F('quantity')),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )

    # cart price summary
    sub_total = (
        cart_items.filter(is_product_active=True, stock_available=True).aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    # --total discount applied-----------------------------------------------------------
    total_discount_amount = cart_items.aggregate(
        total=Coalesce(Sum('discount_subtotal'), Decimal(0.00))
    )['total']

    grand_total = (Decimal(sub_total) - Decimal(total_discount_amount)).quantize(
        Decimal("0.00"), rounding=ROUND_HALF_UP
    )

    # --fetch coupon discount details if applied-----------------------------------
    cart_applied_exist = CartAppliedCoupon.objects.filter(user=user).first()
    coupon_discount = 0
    applied_coupon = None
    if cart_applied_exist:
        applied_coupon = cart_applied_exist.coupon
        if applied_coupon.discount_type == 'FLAT':
            coupon_discount = applied_coupon.discount_value
        elif applied_coupon.discount_type == 'PERCENTAGE':
            coupon_discount = (grand_total * applied_coupon.discount_value) / 100
            coupon_discount = Decimal(coupon_discount).quantize(
                Decimal("0.00"), rounding=ROUND_HALF_UP
            )
        grand_total -= coupon_discount
    
    #---Add 50rs per item as shipping fee to grand total after offer and coupon discounts are applied--
    cart_items_count = cart_items.count()
    delivery_fee_per_item = Decimal(50.00)
    delivery_fee_total = cart_items_count * delivery_fee_per_item
    grand_total += delivery_fee_total

    cart_summary = {
        "sub_total": sub_total,
        "delivery_fee": delivery_fee_total,
        "offer_discount": total_discount_amount,
        "coupon_discount": coupon_discount,
        "grand_total": grand_total,
    }

    return {
        "items": cart_items,
        "cart_summary": cart_summary,
        "applied_coupon": applied_coupon,
    }
