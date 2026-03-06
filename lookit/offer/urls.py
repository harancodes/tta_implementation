from django.urls import path
from . import views

urlpatterns = [
    path("admin/list/", views.admin_list_offers, name="admin-list-offers"),
    path("admin/add-offer/", views.admin_add_offer, name="admin-add-offer"),
    path("admin/edit-offer/<offer_uuid>/", views.admin_edit_offer, name="admin-edit-offer"),
]
