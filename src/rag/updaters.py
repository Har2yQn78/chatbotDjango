from django.apps import apps
from llama_index.core import Document
from .engines import get_model_index
from concurrent.futures import ThreadPoolExecutor

def update_single_document(model_name: str, obj_id: int):
    """Update single document in vector store"""
    model = apps.get_model("data", model_name)
    try:
        obj = model.objects.get(pk=obj_id)
        if not should_include(obj):
            return
            
        doc = Document(
            text=obj.get_embedding_text_raw(),
            doc_id=f"{model_name.lower()}_{obj.id}",
            embedding=obj.embedding.tolist(),
            metadata={
                "model_type": model_name,
                "pk": obj.pk,
                **{field.name: str(getattr(obj, field.name)) 
                   for field in model._meta.fields 
                   if field.name in ['name', 'description']}
            }
        )
        
        index = get_model_index(model_name)
        if index:
            index.delete_ref_doc(doc.doc_id)
            index.insert(doc)
            print(f"Updated {model_name} #{obj_id}")
            
    except Exception as e:
        print(f"Failed updating {model_name} #{obj_id}: {str(e)}")

def batch_update(model_name: str, obj_ids: list[int]):
    """Batch update documents for a specific model"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(
            lambda obj_id: update_single_document(model_name, obj_id),
            obj_ids
        )

def handle_model_update(sender, instance, **kwargs):
    """Signal handler for model updates"""
    model_name = instance.__class__.__name__
    if model_name in ['Employee', 'Product', 'InventoryItem', 'ProductType']:
        update_single_document(model_name, instance.pk)