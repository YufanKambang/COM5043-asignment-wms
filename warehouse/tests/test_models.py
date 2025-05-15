import pytest
from warehouse.models import Product, Supplier, CustomerOrder

@pytest.mark.django_db #wraps my test in a database transaction, which it will roll back after the test finishes
@pytest.mark.parametrize("model_class, create_kwargs", [
    (Product, {"name": "test_product", "description": "it is a test", "stock_quantity": 69, "restock_indicator": 13, "cost_price": 13.69, "selling_price": 27.38}),
    (Supplier, {"name": "test_supplier", "contact_email": "test_supplier@mail.com", "phone": "123", "address": "Atlantis"}),
    (CustomerOrder, {"customer_name": "test_customer", "customer_email": "test_customer@mail.com"}),
]) #this is test data that the test function below will itterate through testing each one
def test_model_create(model_class, create_kwargs):
    #need to test the creation of an object from each class that does not need a foriegn key
    obj = model_class.objects.create(**create_kwargs)
    
    assert str(obj.id) in obj.describe()