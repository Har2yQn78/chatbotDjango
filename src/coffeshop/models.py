from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from pgvector.django import VectorField

from . import services

EMBEDDING_MODEL = "mistral-embed"
EMEDDING_LENGTH = services.EMEDDING_LENGTH

# Define your models and also add embedding
class EmployeeRole(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def get_embedding_text_raw(self):
        return f"{self.name} - {self.description or ''}"
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT)
    hire_date = models.DateField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def get_embedding_text_raw(self):
        return f"{self.name} - {self.role.name}"
    
    def __str__(self):
        return f"{self.name} ({self.role.name})"


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def get_embedding_text_raw(self):
        return f"{self.name} - {self.description}"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    last_indexed = models.DateTimeField(null=True, blank=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def get_embedding_text_raw(self):
        return f"{self.name} - {self.product_type.name} - {self.description}"
    
    def __str__(self):
        return f"{self.name} (${self.price})"


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, help_text="e.g., kg, g, lbs, oz, pieces")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def get_embedding_text_raw(self):
        return f"{self.name} - {self.quantity} {self.unit}"
    
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class ProductInventoryRequirement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_requirements')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ('product', 'inventory_item')
    
    def __str__(self):
        return f"{self.product.name} requires {self.quantity_required} {self.inventory_item.unit} of {self.inventory_item.name}"


# New Models for a More Comprehensive Benchmark

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = f"{self.name} - {self.email} - {self.address or ''}"
            self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = f"{self.name} - {self.address or ''}"
            self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = f"{self.customer.name} - {self.shipping_address}"
            self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.embedding is None:
            raw_embedding_text = f"Order{self.order.id} - {self.product.name} - {self.quantity}"
            self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Item: {self.product.name} in Order #{self.order.id}"
