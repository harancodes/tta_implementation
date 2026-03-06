from order.models import Review
from django.db.models import Count, Avg, Sum
from .models import Product
from order.models import OrderItems

def get_rating_summary(product):
    qs = Review.objects.filter(product=product)

    total_reviews = qs.count()

    # Default response when no reviews
    if total_reviews == 0:
        return {
            'average': 0,
            'total_reviews': 0,
            'breakdown': {i: 0 for i in range(1, 6)},
        }

    # Average rating
    average = qs.aggregate(avg=Avg('rating'))['avg']
    average = round(average, 1)

    # Count per rating
    counts = (
        qs.values('rating')
        .annotate(count=Count('id'))
    )

    # Convert to percentage
    breakdown = {i: 0 for i in range(1, 6)}
    for item in counts:
        rating = item['rating']
        percentage = round((item['count'] / total_reviews) * 100)
        breakdown[rating] = percentage

    return {
        'average': average,
        'total_reviews': total_reviews,
        'breakdown': breakdown,
    }


def fetch_all_reviews(product_id):
    reviews =  Review.objects.filter(product_id=product_id).order_by("-created_at")
    return reviews


def get_top_sellers():
    top_sellers = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED,
            is_active=True,
            variant__stock__gt=0
        )
        .distinct()
        .annotate(
            units_sold=Count('variant__orders'),
        )
        .order_by('-units_sold')[:8]
    )
    return top_sellers