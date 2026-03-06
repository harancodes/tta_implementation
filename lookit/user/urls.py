from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    user_login,
    signup,
    otp_verification,
    user_logout,
    send_otp,
    account_details,
    edit_profile,
    add_address,
    delete_address,
    edit_address,
    change_password,
    address_book,
    set_default_address,
    profile_send_otp,
    change_user_email,
    verify_email,
    wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    wishilst_move_to_cart,
    clear_wishlist,
    toggle_wishlist_ajax,
)

urlpatterns = [
    path("", user_login, name="user-login"),
    path("signup/", signup, name="user-signup"),
    path("signup/otp/", otp_verification, name="signup-otp"),
    path("logout/", user_logout, name="user-logout"),
    path("signup/otp/resend/", send_otp, name='signup-send-otp'),
    path("profile/account-details/", account_details, name='account-details'),
    path("profile/account-details/edit-profile", edit_profile, name='edit-profile'),
    path("add-address/", add_address, name="add-address"),
    path("delete-address/", delete_address, name="delete-address"),
    path("edit-address/", edit_address, name="edit-address"),
    path('change-password/', change_password, name='user-change-password'),
    path('address-book/', address_book, name="address-book"),
    path("set-default-address/<address_id>/", set_default_address, name="set-default-address"),
    path("profile/account-details/send-otp/", profile_send_otp, name="profile-send-otp"),
    path("profile/account-details/change-email/", change_user_email, name="change-user-email"),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    
    path("wishlist/", wishlist, name="wishlist"),
    path("wishlist/add-to-wishlist", add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/remove-from-wishlist", remove_from_wishlist, name="remove-from-wishlist"),
    path("wishlist/move-to-cart/", wishilst_move_to_cart, name="move-to-cart"),
    path("wishlist/clear-wishlist", clear_wishlist, name="clear-wishlist"),
    path("explore/toggle-wishlist-item", toggle_wishlist_ajax, name="toggle-wishlist-item"),
    
    # password reset paths
    # 1.enter email and button for sent link
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name="user/auth/forgot_password.html"
        ),
        name="password-reset",
    ),
    # 2.link sent, check your mail message
    path(
        'password-reset-sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/auth/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    # 3. user click link. django check if it valid. show a form to enter new password
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/auth/reset_password_form.html",
        ),
        name="password_reset_confirm",
    ),
    # 4. show password reset complete message
    path(
        'reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/auth/reset_password_complete.html"
        ),
        name="password_reset_complete",
    ),
]
