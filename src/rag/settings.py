from decouple import config
from llama_index.llms.mistralai import MistralAI

from llama_index.core import Settings

from llama_index.embeddings.mistralai import MistralAIEmbedding



EMEDDING_LENGTH = config("EMEDDING_LENGTH", default=1024, cast=int)
EMEDDING_MODEL =config("EMEDDING_MODEL", default="mistral-embed")
MISTRAL_API_KEY = config("MISTRAL_API_KEY")

VECTOR_DB_NAME = config("VECTOR_DB_NAME", default='vector_db')
VECTOR_DB_TABLE_NAME = config("VECTOR_DB_TABLE_NAME", default='blogpost')

def init():
    llm = MistralAI(api_key=MISTRAL_API_KEY)
    embed_model = MistralAIEmbedding(model=EMEDDING_MODEL, api_key=MISTRAL_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model