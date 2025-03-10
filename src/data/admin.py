from django.contrib import admin
from .models import (
    Category, Product, Inventory,
    Order, OrderItem, Employee, Expense
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'cost', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'unit', 'unit_price', 'reorder_level')
    list_filter = ('unit',)
    search_fields = ('item_name', 'supplier')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'status', 'total_amount', 'payment_method')
    list_filter = ('status', 'payment_method')
    search_fields = ('notes',) 
    inlines = [OrderItemInline]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'hourly_rate', 'hire_date', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'description')
    list_filter = ('category', 'date')
    date_hierarchy = 'date'