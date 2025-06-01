from django.urls import path
from .views import (
    home_page,
    product_list, product_create, product_update, product_delete,
    supplier_list,supplier_create, supplier_update, supplier_delete,
    customer_order_list, order_create, 
    PurchaseOrderReceive, PurchaseOrderCreate, PurchaseOrderList,
    transaction_list, FinanceReportView,
)

urlpatterns = [
    path('', home_page.as_view(), name='home'),

    # product CRUD extras
    path('products/', product_list.as_view(), name='product_list'),
    path('products/new/', product_create.as_view(), name='product_create'),
    path('products/<int:pk>/edit/',  product_update.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', product_delete.as_view(), name='product_delete'),

    # supplier CRUD extras
    path('suppliers/', supplier_list.as_view(), name='supplier_list'),
    path('suppliers/new/', supplier_create.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/edit/',  supplier_update.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', supplier_delete.as_view(), name='supplier_delete'),

    path('customer_orders/', customer_order_list.as_view(), name='customer_order_list'),
    path('customer_orders/new/', order_create, name='customer_order_create'),

    path('purchase_orders/', PurchaseOrderList.as_view(), name='purchase_order_list'),
    path('purchase_orders/new/', PurchaseOrderCreate.as_view(), name='purchase_order_create'),
    path('purchase_orders/<int:pk>/receive/', PurchaseOrderReceive.as_view(), name='purchase_order_receive'),

    path('transactions/', transaction_list.as_view(), name='transaction_list'),
    path('finance/', FinanceReportView.as_view(), name='finance_report'),

]