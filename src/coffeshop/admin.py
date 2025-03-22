from django.contrib import admin
from django.utils.html import format_html
from .models import EmployeeRole, Employee, ProductType, Product, InventoryItem, ProductInventoryRequirement

class ProductInventoryRequirementInline(admin.TabularInline):
    model = ProductInventoryRequirement
    extra = 1
    autocomplete_fields = ['inventory_item']

@admin.register(EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'hire_date', 'hourly_rate', 'is_active')
    list_filter = ('role', 'is_active', 'hire_date')
    search_fields = ('name',)
    autocomplete_fields = ['role']
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'hire_date')
        }),
        ('Employment Details', {
            'fields': ('hourly_rate', 'is_active')
        }),
    )

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count')
    search_fields = ('name',)
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<a href="{}?product_type__id__exact={}">{} products</a>', 
                          '../product/', obj.id, count)
    
    product_count.short_description = 'Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'is_available')
    list_filter = ('product_type', 'is_available')
    search_fields = ('name',)
    autocomplete_fields = ['product_type']
    inlines = [ProductInventoryRequirementInline]
    list_editable = ('price', 'is_available')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'product_type', 'price')
        }),
        ('Details', {
            'fields': ('description', 'is_available')
        }),
    )

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_display', 'unit', 'reorder_level', 'inventory_status')
    list_filter = ('unit',)
    search_fields = ('name',)
    list_editable = ('reorder_level',)
    
    def quantity_display(self, obj):
        return f"{obj.quantity} {obj.unit}"
    
    def inventory_status(self, obj):
        if obj.quantity <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of stock</span>')
        elif obj.quantity < obj.reorder_level:
            return format_html('<span style="color: orange; font-weight: bold;">Low stock</span>')
        else:
            return format_html('<span style="color: green;">In stock</span>')
    
    quantity_display.short_description = 'Quantity'
    inventory_status.short_description = 'Status'

@admin.register(ProductInventoryRequirement)
class ProductInventoryRequirementAdmin(admin.ModelAdmin):
    list_display = ('product', 'inventory_item', 'quantity_required')
    list_filter = ('product', 'inventory_item')
    autocomplete_fields = ['product', 'inventory_item']