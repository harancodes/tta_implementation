from django.shortcuts import render
from product.models import Product
from offer.utiils import annotate_offers
from user.utils import annotate_wishlist_products
from product.utils import get_top_sellers


def home(request):
    user = request.user
    new_arrivals = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('-created_at')[:8]
    new_arrivals = annotate_offers(new_arrivals) #apply offer discounts
        
    
    #featured = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('created_at')[:4]
    featured = get_top_sellers()
    featured = annotate_offers(featured) #apply offer_discounts
    
    if request.user.is_authenticated:
        new_arrivals = annotate_wishlist_products(user, new_arrivals) #for showing in wishlist status 
        featured = annotate_wishlist_products(user, featured) #for showing in wishlist status 
    
    return render(request, "core/index.html",{'user':user, 'new_arrivals': new_arrivals, 'featured':featured})


        