import numpy as np
from mistralai import Mistral
from decouple import config, AutoConfig
from django.apps import apps
from pgvector.django import CosineDistance
from django.db.models import F


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