from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, PurchaseOrder, Transaction, Product

@receiver(post_save, sender=OrderItem)
def adjust_inventory_on_sale(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock_quantity -= instance.quantity
        product.save()

        Transaction.objects.create(
            transaction_type='SALE',
            product=product,
            quantity=instance.quantity,
            amount=instance.subtotal()
        )

@receiver(post_save, sender=PurchaseOrder)
def adjust_inventory_on_purchase(sender, instance, **kwargs):
    if instance.received and not Transaction.objects.filter(
        transaction_type='PURCHASE',
        product=instance.product,
        quantity=instance.quantity,
    ).exists():
        
        product = instance.product
        product.stock_quantity += instance.quantity
        product.save()

        Transaction.objects.create(
            transaction_type='PURCHASE',
            product=product,
            quantity=instance.quantity,
            amount=instance.quantity * product.cost_price
        )