from django.urls import path
from .views import (
    admin_list_products,
    admin_add_product,
    admin_edit_product,
    admin_list_categories,
    admin_add_style,
    admin_delete_category,
    admin_restore_category,
    admin_edit_category,
    admin_view_product,
    admin_toggle_product_active,
    admin_manage_stocks,
    admin_update_stock,
    admin_delete_variant,
    
    product_details,
    explore,
    add_to_cart,
)

urlpatterns = [
    path("admin/list/", admin_list_products, name="admin-list-products"),
    path("admin/add-product/", admin_add_product, name="admin-add-product"),
    path("admin/edit-product/<product_uuid>/", admin_edit_product, name="admin-edit-product"),
    path("admin/view-product/<product_uuid>", admin_view_product, name="admin-view-product"),
    path("admin/toggle-product-active/<product_uuid>/", admin_toggle_product_active, name="admin_toggle_product_active"),
    path("admin/manage-stocks/<product_uuid>", admin_manage_stocks, name="admin-manage-stocks"),
    path("admin/update-stocks", admin_update_stock, name="admin-update-stock"),
    path("admin/delete_variant/<variant_id>", admin_delete_variant, name="admin-delete-variant"),
    
    path(
        "admin/category/list",
        admin_list_categories,
        name='admin-category-management',
    ),
    path("admin/category/add-style", admin_add_style, name="admin-add-style"),
    path("admin/category/delete-style/<style_id>", admin_delete_category, name="admin-delete-category"),
    path("admin/category/restore-style/<style_id>", admin_restore_category, name="admin-restore-category"),
    path("admin/category/edit-style/", admin_edit_category, name="admin-edit-category"),
    
    path("product-details/<product_uuid>/",product_details, name="product-details"),
    path("explore/", explore, name="explore"),
    path("add-to-cart/", add_to_cart, name="add-to-cart")

]
