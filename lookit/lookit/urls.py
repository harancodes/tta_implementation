from django.urls import path, include

urlpatterns = [
    path("user/",include('user.urls')),
    path("",include('core.urls')),
    path("admin/", include('staff.urls')),
    path("product/", include('product.urls')),
    path("cart/", include('cart.urls')),
    path("order/", include('order.urls')),
    path("payment/", include('payment.urls')),
    path('wallet/', include('wallet.urls')),
    path('coupon/', include('coupon.urls')),
    path('offer/', include('offer.urls')),
        # continue with google
    path('oauth/', include('social_django.urls', namespace='social')),
]
