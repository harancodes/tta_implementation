from django.urls import path
from . import views

urlpatterns = [
    path("admin/list/", views.admin_list_coupon, name="admin-list-coupons"),
    path("admin/add-coupon", views.admin_add_coupon, name="admin-add-coupon"),
    path("admin/edit-coupon/<slug:code>/", views.admin_edit_coupon, name="admin-edit-coupon"),
]
