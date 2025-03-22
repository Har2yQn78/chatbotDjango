import numpy as np
from mistralai import Mistral
from decouple import config, AutoConfig
from django.apps import apps
from pgvector.django import CosineDistance
from django.db.models import F, Q


config = AutoConfig(search_path="/home/harry/chatbotDjango") 
MISTRAL_API_KEY = config("MISTRAL_API_KEY")
model = "mistral-embed"
EMEDDING_LENGTH=config("EMEDDING_LENGTH", default=1024, cast=int)
client = Mistral(api_key=MISTRAL_API_KEY)


def get_embedding(texts, model=model):
    if not isinstance(texts, list):
        texts = [texts]
        single_text = True
    else:
        single_text = False
    cleaned_texts = [t.replace("\n", "").strip() for t in texts]
    response = client.embeddings.create(model=model, inputs=cleaned_texts)
    embeddings = np.array([entry.embedding for entry in response.data])
    return embeddings[0] if single_text else embeddings


def get_query_embedding(text):
    return get_embedding(text)


def search_posts(query, limit=5):
    BlogPost = apps.get_model(app_label='data', model_name='BlogPost')
    query_embedding = get_query_embedding(query)
    qs = BlogPost.objects.annotate(
        distance=CosineDistance('embedding', query_embedding),
        similarity=1 - F("distance")
        ).order_by("distance")[:limit]
    return qs


# Coffee Shop Services
def search_products_by_text(query, limit=10):
    """
    Search products using vector similarity with MistralAI embeddings.
    """
    Product = apps.get_model(app_label='data', model_name='Product')
    query_embedding = get_query_embedding(query)
    
    products = Product.objects.annotate(
        distance=CosineDistance('embedding', query_embedding),
        similarity=1 - F("distance")
    ).order_by("distance")[:limit]
    
    return products


def search_inventory_by_text(query, limit=10):
    """
    Search inventory items using vector similarity with MistralAI embeddings.
    """
    InventoryItem = apps.get_model(app_label='data', model_name='InventoryItem')
    query_embedding = get_query_embedding(query)
    
    items = InventoryItem.objects.annotate(
        distance=CosineDistance('embedding', query_embedding),
        similarity=1 - F("distance")
    ).order_by("distance")[:limit]
    
    return items


def search_employees_by_text(query, limit=10):
    """
    Search employees using vector similarity with MistralAI embeddings.
    """
    Employee = apps.get_model(app_label='data', model_name='Employee')
    query_embedding = get_query_embedding(query)
    
    employees = Employee.objects.annotate(
        distance=CosineDistance('embedding', query_embedding),
        similarity=1 - F("distance")
    ).order_by("distance")[:limit]
    
    return employees


def get_low_inventory_items():
    """
    Get inventory items that are below reorder level.
    """
    InventoryItem = apps.get_model(app_label='data', model_name='InventoryItem')
    
    items = InventoryItem.objects.filter(
        quantity__lt=F('reorder_level')
    )
    
    return items


def check_product_availability(product_id):
    """
    Check if a product can be made based on current inventory.
    """
    Product = apps.get_model(app_label='data', model_name='Product')
    ProductInventoryRequirement = apps.get_model(app_label='data', model_name='ProductInventoryRequirement')
    
    try:
        product = Product.objects.get(id=product_id)
        requirements = ProductInventoryRequirement.objects.filter(product=product)
        
        can_make = True
        missing_items = []
        
        for req in requirements:
            if req.inventory_item.quantity < req.quantity_required:
                can_make = False
                missing_items.append({
                    'item': req.inventory_item.name,
                    'required': float(req.quantity_required),
                    'available': float(req.inventory_item.quantity),
                    'unit': req.inventory_item.unit
                })
        
        return {
            'product': product.name,
            'can_make': can_make,
            'missing_items': missing_items
        }
    except Product.DoesNotExist:
        return {'error': 'Product not found'}


def get_products_by_type(product_type_id):
    """
    Get all products of a specific product type.
    """
    Product = apps.get_model(app_label='data', model_name='Product')
    
    products = Product.objects.filter(
        product_type_id=product_type_id,
        is_available=True
    ).order_by('name')
    
    return products


def get_all_product_types():
    """
    Get all product types for dropdown menus.
    """
    ProductType = apps.get_model(app_label='data', model_name='ProductType')
    
    return ProductType.objects.all().order_by('name')


def get_employee_by_role(role_id):
    """
    Get all employees with a specific role.
    """
    Employee = apps.get_model(app_label='data', model_name='Employee')
    
    employees = Employee.objects.filter(
        role_id=role_id,
        is_active=True
    ).order_by('name')
    
    return employees