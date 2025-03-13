import numpy as np
from mistralai import Mistral
from decouple import config, AutoConfig


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