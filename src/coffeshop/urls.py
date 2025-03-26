from django.urls import path
from . import views

app_name = 'coffeshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/update/<int:item_id>/', views.update_inventory, name='update_inventory'),
    path('employees/', views.employee_list, name='employee_list'),
]