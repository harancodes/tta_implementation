from .models import Cart
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def validate_cart(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        #ensure cart is not empty
        cart_count = Cart.objects.filter(user=request.user).count()
        if cart_count == 0:
            messages.error(request, "Cart is empty — please add items to continue")
            return redirect('cart')
        
        #ensure no out of stock product in cart
        out_of_stock_products = Cart.objects.filter(variant__stock__lte = 0)
        if out_of_stock_products.exists():
            messages.error(request, f"{out_of_stock_products[0].product.name} is out of stock")
            return redirect('cart')
        
        #ensure no unavailble products
        unavailable_products = Cart.objects.filter(variant__product__is_active = False)
        if unavailable_products.exists():
            messages.error(request, f"{unavailable_products[0].product.name} is unavailable")
            return redirect('cart')
        
        return view_func(request, *args, **kwargs)
    return wrapper
