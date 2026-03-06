from django.utils import timezone
from django.db.models import (
    OuterRef,
    Subquery,
    Max,
    Value,
    IntegerField,
    ExpressionWrapper,
    F,
    DecimalField,
    Case,
    When,
    CharField,
)
from django.db.models.functions import Round, Coalesce, Greatest
from .models import Offer
from django.utils import timezone


def annotate_offers(product_query_set):
    """function which annotate largest available offer price to each product if available and return the query set"""
    # sub queries for fetching offers
    today = timezone.now().date()

    product_discount_sq = (
        Offer.objects.filter(
            products=OuterRef('pk'),
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
            style=OuterRef('style'),
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .values('style')
        .annotate(max_discount=Max('discount'))
        .values('max_discount')[:1]
    )

    offer_annotated_products_set = (
        product_query_set.annotate(
            product_discount=Coalesce(
                Subquery(product_discount_sq), Value(0), output_field=IntegerField()
            ),
            category_discount=Coalesce(
                Subquery(category_discount_sq), Value(0), output_field=IntegerField()
            ),
        )
        .annotate(
            offer_percentage=Greatest(F('product_discount'), F('category_discount'))
        )
        .annotate(
            offer_deduction_amount=ExpressionWrapper(
                Round((F('price') * F('offer_percentage') / Value(100)), 2),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        .annotate(
            offer_price=ExpressionWrapper(
                Round(F('price') - F('offer_deduction_amount'), 2),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )
    return offer_annotated_products_set


def annotate_offer_status(offer_set):
    """function to find and annotate offer status to each offer in the query set"""
    today = timezone.now().date()
    
    status_annotated_offer_set = offer_set.annotate(status=Case(
        When(is_active=False, then=Value('inactive')),
        When(start_date__gt=today, then=Value('upcoming')),
        When(end_date__lt=today, then=Value('ended')),
        default=Value('active'),
        output_field=CharField()
    ))
    return status_annotated_offer_set