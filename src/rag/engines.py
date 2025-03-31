from typing import List
from django.apps import apps
from sqlalchemy import make_url, create_engine
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.retrievers import NLSQLRetriever

from . import db, settings, prompts

EMBEDDING_LENGTH = settings.EMBEDDING_LENGTH 

settings.init()

def get_vector_store(model_name: str):
    """Get vector store for a specific model"""
    db_url = db.get_database_url(use_pooling=True)
    url = make_url(db_url)
    
    # Get table name from model naming convention
    table_name = f"{model_name.lower()}s"
    
    return PGVectorStore.from_params(
        database=settings.VECTOR_DB_NAME,
        host=url.host,
        password=url.password,
        port=url.port or 5432,
        user=url.username,
        table_name=table_name,
        embed_dim=EMBEDDING_LENGTH,
    )

def get_model_index(model_name: str):
    """Get index for specific model"""
    vector_store = get_vector_store(model_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

def get_semantic_query_engine(model_name: str):
    """Get query engine for specific model"""
    index = get_model_index(model_name)
    return index.as_query_engine()

def get_default_sql_engine_tables() -> List[str]:
    """Get relevant coffee shop tables for SQL engine"""
    models = [
        apps.get_model("coffeshop", "EmployeeRole"),
        apps.get_model("coffeshop", "Employee"),
        apps.get_model("coffeshop", "ProductType"),
        apps.get_model("coffeshop", "Product"),
        apps.get_model("coffeshop", "InventoryItem"),
        apps.get_model("coffeshop", "ProductInventoryRequirement")
    ]
    return [model._meta.db_table for model in models]

def get_llamaindex_sql_database() -> SQLDatabase:
    """Create SQLDatabase instance for coffee shop models"""
    tables = get_default_sql_engine_tables()
    database_url = db.get_database_url(use_pooling=True)
    engine = create_engine(database_url)
    return SQLDatabase(engine, include_tables=tables)

def get_sql_query_engine(*args, **kwargs) -> NLSQLTableQueryEngine:
    """Create SQL query engine with coffee shop context"""
    sql_database = get_llamaindex_sql_database()
    config = {
        "sql_database": sql_database,
        "tables": get_default_sql_engine_tables(),
        "response_synthesis_prompt": prompts.custom_sql_response_synthesis_prompt,
        "text_to_sql_prompt": prompts.custom_text_to_sql_prompt
    }
    config.update(**kwargs)
    return NLSQLTableQueryEngine(*args, **config)

def get_sql_query_retriever(*args, **kwargs) -> NLSQLRetriever:
    """Create SQL retriever for coffee shop data"""
    sql_database = get_llamaindex_sql_database()
    config = {
        "sql_database": sql_database,
        "tables": get_default_sql_engine_tables(),
        "response_synthesis_prompt": prompts.custom_sql_response_synthesis_prompt,
        "text_to_sql_prompt": prompts.custom_text_to_sql_prompt
    }
    config.update(**kwargs)
    return NLSQLRetriever(*args, **config)