from django.urls import path
from .views import (
    checkout,
    payment_page,
    create_order,
    place_order,
    order_success_page,
    my_orders,
    track_order,
    admin_list_orders,
    admin_order_details,
    admin_update_delivery_status,
    cancel_order,
    admin_list_return_requests,
    return_request_form,
    track_return_request,
    admin_return_details,
    admin_update_return_status,
    download_invoice_pdf,
    payment_failure_page,
    sales_report,
    download_sales_report_pdf,
    export_sales_report_excel,
    write_review,
)

#urls of order app
urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("create-order/", create_order, name="create_order"),
    path("payment/<order_uuid>/", payment_page, name="payment-page"),
    path("place-order/<order_uuid>/", place_order, name="place-order"),
    path("order-success/<order_uuid>/", order_success_page, name="order-success"),
    path("payment-failure/<order_uuid>/", payment_failure_page, name="payment-failed"),
    path("my-orders/", my_orders, name="my-orders"),
    path("track-order/<order_uuid>/", track_order, name="track-order"),
    path('invoice/<order_uuid>/', download_invoice_pdf, name='invoice'),
    path("write-review/<order_uuid>/", write_review, name="write-review"),
    
    path("admin/list-orders/", admin_list_orders, name="admin-list-orders"),
    path("admin/order-details/<order_item_uuid>/", admin_order_details, name="admin-order-details"),
    path("admin/update-delivery-status/<order_item_uuid>/", admin_update_delivery_status, name="update-delivery-status"),
    path("cancel-order/<order_item_uuid>/", cancel_order, name="cancel-order"),
    path("admin/return-request/list/", admin_list_return_requests, name="admin-list-return-requests"),
    
    #return
    path("return-request-form/<order_uuid>/", return_request_form, name="return-request-form"),
    path("track-return-request/<order_uuid>/", track_return_request, name="track_return_request"),
    path("admin/return-request/return-details/<return_request_uuid>/", admin_return_details, name="admin-return-details"),
    path("admin/return-request/update-return-status/<return_request_uuid>/", admin_update_return_status, name="admin-update-return-status"),
    
    path("admin/sales-report/", sales_report, name="admin-sales-report"),
    path("admin/reports/sales/pdf/", download_sales_report_pdf, name="sales-report-pdf"),
    path("admin/reports/sales/excel/", export_sales_report_excel, name="sales-report-excel"),

]
