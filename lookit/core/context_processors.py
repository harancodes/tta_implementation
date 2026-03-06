from cart.models import Cart
from user.models import Wishlist

#context preprocessor for showing cart count as badge in every page
def cart_item_count(request):
    cart_count = Cart.objects.filter(user__id=request.user.id).count()
    wishlist_count = Wishlist.objects.filter(user__id=request.user.id).count()
    context = {
        "cart_count":cart_count,
        "wishlist_count": wishlist_count,
    }    
    return context