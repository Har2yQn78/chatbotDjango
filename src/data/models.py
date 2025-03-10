from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], help_text="Cost to make the product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    is_available = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def __str__(self):
        return str(self.name)


class Inventory(models.Model):
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=50, help_text="e.g., kg, lbs, oz, bags, etc.")
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    supplier = models.CharField(max_length=200, blank=True)
    supplier_contact = models.CharField(max_length=200, blank=True)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    last_ordered = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.unit}"
    
    class Meta:
        verbose_name_plural = "Inventory Items"


class Order(models.Model):
    id = models.AutoField(primary_key=True)  
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('mobile_payment', 'Mobile Payment'),
    )
    
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    customizations = models.TextField(blank=True, help_text="e.g., extra shot, less sugar")
    

class Employee(models.Model):
    ROLES = (
        ('barista', 'Barista'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('cleaner', 'Cleaner'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    hire_date = models.DateField()
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=200, blank=True)



class Expense(models.Model):
    EXPENSE_CATEGORIES = (
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('inventory', 'Inventory'),
        ('salaries', 'Salaries'),
        ('equipment', 'Equipment'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    )
    
    date = models.DateField()
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    receipt = models.FileField(upload_to='expenses/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.category} - ${self.amount} on {self.date}"