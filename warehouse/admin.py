from django.contrib import admin
from .models import Product, Supplier, PurchaseOrder, CustomerOrder, OrderItem, Transaction

# Register your models here.
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(CustomerOrder)
admin.site.register(OrderItem)
admin.site.register(Transaction)