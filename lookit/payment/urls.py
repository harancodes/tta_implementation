from django.urls import path
from payment import views

urlpatterns = [
    path('paymenthandler/', views.paymenthandler, name='razorpay_paymenthandler'),
    path("create_razorpay_order/", views.create_razorpay_order, name="create_razorpay_order"),
    path("create-wallet-topup/", views.create_razorpay_wallet_topup, name="create-wallet-topup"),
    path("wallet-topup-payment-handler/", views.wallet_topup_paymenthandler, name="wallet-topup-payment-handler"),
]