# from decouple import config
# from openai import OpenAI
# from llama_index.core import Settings
# from llama_index.llms.openrouter import OpenRouter
# from llama_index.embeddings.mistralai import MistralAIEmbedding

# VECTOR_DB_NAME = config("VECTOR_DB_NAME", default='vector_db')
# MODELS = [
#     "EmployeeRole",
#     "Employee",
#     "ProductType",
#     "Product", 
#     "InventoryItem",
#     "ProductInventoryRequirement"
# ]
# VECTOR_DB_TABLE_NAMES = [f"{model.lower()}s" for model in MODELS]
# EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=1024, cast=int)
# EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="mistral-embed")
# MISTRAL_API_KEY = config("MISTRAL_API_KEY")
# LLM_API_KEY = config("LLM_API_KEY")
# SITE_URL = config("SITE_URL", default="")
# SITE_NAME = config("SITE_NAME", default="")
# LLM_MODEL = config("LLM_MODEL", default="oogle/gemma-3-27b-it:free")

# def init():
#     llm = OpenRouter(
#         model=LLM_MODEL,
#         api_key=LLM_API_KEY,
#         http_referer=SITE_URL,
#         title=SITE_NAME
#     )

#     embed_model = MistralAIEmbedding(
#         model=EMBEDDING_MODEL,
#         api_key=MISTRAL_API_KEY,
#         embed_dim=EMBEDDING_LENGTH
#     )
    
#     Settings.llm = llm
#     Settings.embed_model = embed_model
    
#     openrouter_client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=LLM_API_KEY,
#     )
    
#     return openrouter_client


from decouple import config
from llama_index.llms.mistralai import MistralAI
from llama_index.core import Settings
from llama_index.embeddings.mistralai import MistralAIEmbedding

# Add the models from your models.py for tables
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