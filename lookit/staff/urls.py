from django.urls import path
from .views import (
    admin_login,
    admin_dashboard,
    admin_logout,
    admin_user_management,
    admin_view_user,
    admin_edit_user,
    admin_add_staff,
    admin_view_staff,
    admin_block_user_toggle,
)


urlpatterns = [
    path("login/", admin_login, name="admin-login"),
    path("", admin_dashboard, name="admin-dashboard"),
    path("logout/", admin_logout, name="admin-logout"),
    
    path("user/list/", admin_user_management, name="admin-user"),
    path("user/view-user/<user_id>", admin_view_user, name="admin-view-user"),
    path("user/edit-user/<user_id>/", admin_edit_user, name="admin-edit-user"),
    path("user/add-staff/", admin_add_staff, name="admin-add-staff"),
    path("user/view-staff/<staff_id>", admin_view_staff, name="admin-view-staff"),
    path("user/block-user-toggle/<user_id>", admin_block_user_toggle, name="admin-block-user-toggle"),
    
]
