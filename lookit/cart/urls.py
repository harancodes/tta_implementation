from django.urls import path
from .views import cart, remove_cart_item, update_quantity, save_coupon, apply_coupon, remove_coupon

urlpatterns = [
    path("", cart, name='cart'),
    path("remove-item/", remove_cart_item, name="remove_cart_item"),
    path("update-quantity/", update_quantity, name="update-quantity"),
    path("save-coupon/", save_coupon, name="save-coupon"),
    path("apply-coupon/", apply_coupon, name="apply-coupon"),
    path("remove-coupon/", remove_coupon, name="remove-coupon"),
]