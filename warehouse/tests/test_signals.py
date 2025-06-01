"""This is to testing the functionality at  warehouse/signals.py"""


import pytest
from warehouse.models import Product, Supplier, PurchaseOrder, Transaction

# this test in hindsite i think may benefit with being split into two different tests
# test that when the wms recieves a purchase order, that it will update the socks and then log the transaction that has occured
@pytest.mark.django_db
def test_receiving_purchase_order_updates_stock_and_logs_transaction():
    supplier = Supplier.objects.create(
        name="Test", contact_email="x@x.com", phone="1", address="x"
    )
    product = Product.objects.create(
        name="Drill", stock_quantity=10, restock_indicator=5,
        cost_price=10.00, selling_price=20.00
    )

    purchase_order = PurchaseOrder.objects.create(
        product=product, quantity=5, supplier=supplier
    )

    assert product.stock_quantity == 10
    
    purchase_order.received = True
    purchase_order.save()

    product.refresh_from_db()
    assert product.stock_quantity == 15

    transaction = Transaction.objects.get(
        product=product, transaction_type="PURCHASE"
    )

    assert transaction.quantity == 5
    assert transaction.amount == 50.00