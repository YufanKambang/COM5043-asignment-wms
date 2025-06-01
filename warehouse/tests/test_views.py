"""This is to testing the functionality at  warehouse/views.py"""


import pytest

from django.urls import reverse
from warehouse.models import Product, Transaction, Supplier

# note here on the arugement client int his test, is a built in pytest ficture that lets us simulate a HTTP client
# leting us perfom GET and POST requests, check status codes, read HTML content on page, assert the page loads correctly and shows expected data to the user
# 
@pytest.mark.django_db
def test_finance_report_totals(client):
    product = Product.objects.create(
        name="Test P", stock_quantity=10, restock_indicator=2,
        cost_price=4.00, selling_price=8.00,
    )

    # generating a sale and a purchase transaction
    Transaction.objects.create(
        product=product, transaction_type="SALE", quantity=2, amount=16.0
    )
    Transaction.objects.create(
        product=product, transaction_type="PURCHASE", quantity=3, amount=12.0
        )
    
    # this is simulating visiting /finance/ using a reverse lookup from the URL patter
    # where name='finance_report', in our warehouse/urls.py
    response = client.get(reverse("finance_report"))
    # comfirming that the page loaded sucessfully and not with a 404 error or a crash
    assert response.status_code == 200

    # this part converts the HTML response from bytes into a string we are able to seach through it
    # this is very helpful for when we want to assert qualities about the page
    content = response.content.decode()

    assert '<p class="card-text" id="sales_total">£16.00</p>' in content
    assert '<p class="card-text" id="purchase_total">£12.00</p>' in content
    assert '<p class="card-text" id="net_income">£4.00</p>' in content