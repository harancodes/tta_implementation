from .models import OrderItems, Review
from product.models import Variant
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Exists, OuterRef, BooleanField, Case, When, Value, Q, F


def reduce_stock_for_order(order_id):
    order_items = OrderItems.objects.select_for_update().filter(order_id=order_id)
    for item in order_items:
        updated = (
            Variant.objects.filter(id=item.variant.id, stock__gte = item.quantity).update(stock=F('stock') - item.quantity)
        )
        if not updated:
            raise ValueError(f"{item.variant.product.name} is out of stock")
        
def restock_inventory(order_item_uuid):
    """function to add stock back to product on cancel and return"""
    order_item = OrderItems.objects.get(uuid = order_item_uuid)
    updated = Variant.objects.filter(id=order_item.variant.id).update(stock = F('stock') + order_item.quantity)
    if updated != 1:
        raise RuntimeError("Failed to restock inventory")

        
def check_stock_and_availability_for_order(order):
    for item in order.items.select_related("variant"):
        if item.variant.stock < item.quantity or not item.product.is_active:
            raise ValueError(
                f"{item.variant.product.name} is out of stock or unavailable"
            )

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.CreatePDF(src=html, dest=result)

    if pdf.err:
        return None

    return result.getvalue()


def annotate_review_eligibility(user, orders_qs):
    """
    1] A user can give review for a product only once
    2] A user can only review product while it's status is delivered
    """
    reviewed_sq = Review.objects.filter(
        user=user,
        product=OuterRef('variant__product')
    )

    annotated_orders_qs = orders_qs.annotate(
        reviewed=Exists(reviewed_sq)
    ).annotate(
        review_eligible=Case(
            When(
                Q(order_status='DELIVERED') & ~F('reviewed'),
                then=Value(True)
            ),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    return annotated_orders_qs
