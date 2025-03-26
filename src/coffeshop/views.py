from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from .models import (
    EmployeeRole, Employee, ProductType, 
    Product, InventoryItem, ProductInventoryRequirement
)

def index(request):
    """Home page view for the coffee shop."""
    context = {
        'product_count': Product.objects.filter(is_available=True).count(),
        'employee_count': Employee.objects.filter(is_active=True).count(),
        'inventory_low': InventoryItem.objects.filter(quantity__lt=Sum('reorder_level')).count(),
    }
    return render(request, 'coffeshop/index.html', context)

@login_required
def product_list(request):
    """View all products with filtering options."""
    products = Product.objects.all()
    product_types = ProductType.objects.all()
    product_type_id = request.GET.get('type')
    if product_type_id:
        products = products.filter(product_type_id=product_type_id)

    availability = request.GET.get('available')
    if availability:
        is_available = availability == 'true'
        products = products.filter(is_available=is_available)
    
    context = {
        'products': products,
        'product_types': product_types,
    }
    return render(request, 'coffeshop/product_list.html', context)

def product_detail(request, product_id):
    """View details of a specific product."""
    product = get_object_or_404(Product, id=product_id)
    requirements = product.inventory_requirements.all()
    
    context = {
        'product': product,
        'requirements': requirements,
    }
    return render(request, 'coffeshop/product_detail.html', context)

def inventory_list(request):
    inventory_items = InventoryItem.objects.all()
    in_stock_count = inventory_items.filter(quantity__gt=F('reorder_level')).count()
    low_stock_count = inventory_items.filter(quantity__lt=F('reorder_level'), quantity__gt=0).count()
    out_of_stock_count = inventory_items.filter(quantity__lte=0).count()
    
    context = {
        'inventory_items': inventory_items,
        'in_stock_count': in_stock_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    
    return render(request, 'coffeshop/inventory_list.html', context)

@login_required
def update_inventory(request, item_id):
    """Update inventory quantity."""
    if request.method == 'POST':
        item = get_object_or_404(InventoryItem, id=item_id)
        try:
            new_quantity = float(request.POST.get('quantity', 0))
            item.quantity = new_quantity
            item.save()
            return redirect('coffeshop:inventory_list')
        except ValueError:
            pass
    
    return redirect('coffeshop:inventory_list')

@login_required
def employee_list(request):
    """View all employees with filtering by role."""
    employees = Employee.objects.all()
    roles = EmployeeRole.objects.all()
    
    role_id = request.GET.get('role')
    if role_id:
        employees = employees.filter(role_id=role_id)
    status = request.GET.get('status')
    if status:
        is_active = status == 'active'
        employees = employees.filter(is_active=is_active)
    
    context = {
        'employees': employees,
        'roles': roles,
        'admin_url': '/admin/coffeshop/employee/add/',  
    }
    return render(request, 'coffeshop/employee_list.html', context)
