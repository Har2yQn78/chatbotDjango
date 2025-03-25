from django.apps import apps
from llama_index.core import Document
from .engines import get_model_index
from datetime import datetime

def should_include(obj) -> bool:
    if hasattr(obj, 'is_active') and not obj.is_active:
        return False
    if hasattr(obj, 'is_available') and not obj.is_available:
        return False
    if hasattr(obj, 'embedding'):
        if obj.embedding is None or len(obj.embedding) == 0:
            return False
    return True


relevant_models = [
    'Employee', 
    'ProductType',
    'Product',
    'InventoryItem'  
]
metadata_fields = {
    'Employee': ['name', 'role', 'hire_date', 'hourly_rate'],
    'ProductType': ['name', 'description'],
    'Product': ['name', 'price', 'description'],
    'InventoryItem': ['name', 'quantity', 'unit']
}
def get_all_docs():
    docs = []
    for model_name in relevant_models:
        model = apps.get_model("coffeshop", model_name)
        qs = model.objects.all()
        for obj in qs:
            if not should_include(obj):
                continue     
            docs.append(Document(
                text=obj.get_embedding_text_raw(),
                doc_id=f"{model_name.lower()}_{obj.id}",
                embedding=obj.embedding.tolist() if obj.embedding is not None else None,
                metadata={
                    "model_type": model_name,
                    "pk": obj.pk,
                    "last_updated": datetime.now().isoformat(),
                    **{
                        field.name: str(getattr(obj, field.name))
                        for field in model._meta.fields
                        if field.name in metadata_fields[model_name]
                    }
                }
            ))
    return docs

def full_sync():
    """Full synchronization across all models"""
    docs = get_all_docs()
    print(f"Starting sync for {len(docs)} documents across all models")
    
    for doc in docs:
        model_name = doc.metadata["model_type"]
        index = get_model_index(model_name)
        
        if index:
            try:
                index.delete_ref_doc(doc.doc_id)
                index.insert(doc)
                if hasattr(index, 'update_model_timestamp'):
                    index.update_model_timestamp(doc.metadata["pk"])
            except Exception as e:
                print(f"Failed syncing {doc.doc_id}: {str(e)}")
    
    print("Full synchronization completed")