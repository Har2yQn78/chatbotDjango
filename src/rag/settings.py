from decouple import config
from llama_index.llms.mistralai import MistralAI
from llama_index.core import Settings
from llama_index.embeddings.mistralai import MistralAIEmbedding

VECTOR_DB_NAME = config("VECTOR_DB_NAME", default='vector_db')
MODELS = [
    "EmployeeRole",
    "Employee",
    "ProductType",
    "Product", 
    "InventoryItem",
    "ProductInventoryRequirement"
]
VECTOR_DB_TABLE_NAMES = [f"{model.lower()}s" for model in MODELS]
EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=1024, cast=int)
EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="mistral-embed")
MISTRAL_API_KEY = config("MISTRAL_API_KEY")

def init():
    llm = MistralAI(api_key=MISTRAL_API_KEY)
    embed_model = MistralAIEmbedding(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY,
        embed_dim=EMBEDDING_LENGTH
    )
    Settings.llm = llm
    Settings.embed_model = embed_model