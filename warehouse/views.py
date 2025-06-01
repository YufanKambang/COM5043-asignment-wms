from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Product, Supplier, CustomerOrder, OrderItem, Transaction, PurchaseOrder

# using inlineformset_formfactory here to create a (set-of/multiple) forms
order_item_formset = inlineformset_factory(
    CustomerOrder,
    OrderItem,
    fields=['product', 'quantity'],
    extra=1, can_delete=False
)
# the code block above creates a reuseable formset class 
# that handles multiple OrderItem enteries or a single CustomerOrder

# Create your views here.
# --- Home Page ---
class home_page(TemplateView):
    template_name = 'warehouse/home.html'

# --- Products ---
class product_list(ListView):
    # this model will use the class stated
    model = Product
    # chooses what template to use for this view page
    template_name = 'warehouse/product_list.html'
    context_object_name = 'products'

class product_create(CreateView):
    model = Product
    fields = [
        'name', 'description', 'stock_quantity',
        'restock_indicator', 'cost_price', 'selling_price'
    ]
    success_url = reverse_lazy('product_list')
    # this is in built Django and used in its class-based views like createView 
    # it defines where to redirect the user after a successful form submission
    template_name = 'warehouse/form.html'

class product_update(UpdateView):
    model = Product
    fields = [
        'name', 'description', 'stock_quantity',
        'restock_indicator', 'cost_price', 'selling_price'
    ]
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('product_list')

class product_delete(DeleteView):
    model = Product
    template_name = 'warehouse/confirm_delete.html'
    success_url = reverse_lazy('product_list')

# --- supplier ---
class supplier_list(ListView):
    model = Supplier
    template_name = 'warehouse/supplier_list.html'
    context_object_name = 'suppliers'

class supplier_create(CreateView):
    model = Supplier
    fields = ['name', 'contact_email', 'phone', 'address']
    success_url = reverse_lazy('supplier_list')
    template_name = 'warehouse/form.html'

class supplier_update(UpdateView):
    model = Supplier
    fields = ['name', 'contact_email', 'phone', 'address']
    success_url = reverse_lazy('supplier_list')
    template_name = 'warehouse/form.html'

class supplier_delete(DeleteView):
    model = Supplier
    template_name = 'warehouse/confirm_delete.html'
    success_url = reverse_lazy('supplier_list')

# --- Customer Orders ---
class customer_order_list(ListView):
    model = CustomerOrder
    template_name = 'warehouse/customer_order_list.html'
    context_object_name = 'orders'

def order_create(request):
    if request.method == 'POST':
        # building formset with the submitted POSt data, if it exists
        formset = order_item_formset(request.POST)

        # builds and holds a new CustomerOrder from the plain inputs from the HTML form
        # manully extracting values from request.POST
        order = CustomerOrder(
            customer_name=request.POST['customer_name'],
            customer_email=request.POST['customer_email']
        )

        if formset.is_valid():
            # now the CustomerOrder held previously is saved into the database
            order.save()

            # creating a list of unsaved OrderItems objects
            # the setting .save(commit=False), validates form, create instances of OrderItems 
            # And does not save them to the database yet
            items = formset.save(commit=False)

            # OrderItems objects require a foreign key that is connected to a CustomerOrder object
            # the reason for saving them later is when the formset is subittted, django doesnt know
            # which order the items belongs too
            for item in items:
                item.order = order
                item.price_at_order = item.product.selling_price
                item.save()
            return redirect('customer_order_list')
    
    else:
        # when the first opened, shown one blank OrderItem form as defualt
        formset = order_item_formset()
    # renders the template with the formset so the user can fill in order items
    return render(
        request, 'warehouse/order_form.html', {
            'formset': formset,
        }
    )

class PurchaseOrderList(ListView):
    model = PurchaseOrder
    template_name = 'warehouse/purchase_order_list.html'
    context_object_name = 'purchase_orders'

class PurchaseOrderCreate(CreateView):
    model = PurchaseOrder
    fields = ['product', 'quantity', 'supplier']
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('purchase_order_list')

class PurchaseOrderReceive(UpdateView):
    model = PurchaseOrder
    fields = ['received']
    template_name = 'warehouse/receive_form.html'
    success_url = reverse_lazy('purchase_order_list')

# --- transaction list ---
class transaction_list(ListView):
    model = Transaction
    template_name = 'warehouse/transaction_list.html'
    context_object_name = 'transactions'

class FinanceReportView(TemplateView):
    template_name = 'warehouse/finance_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sales_total = Transaction.objects.filter(
            transaction_type='SALE'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        purchase_total = Transaction.objects.filter(
            transaction_type='PURCHASE'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        net_income = sales_total - purchase_total

        context.update({
            'sales_total': sales_total,
            'purchase_total': purchase_total,
            'net_income': net_income,
            'transactions': Transaction.objects.order_by('-date')[:20],  # optional
        })
        return context
