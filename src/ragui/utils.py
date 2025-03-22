from rag import (
    db as rag_db,
    engines as rag_engines,
    settings as rag_settings,
    updaters as rag_updaters,
    patches as rag_patches,
)
from llama_index.core.tools import QueryEngineTool
import io
import sys

def initialize_rag():
    rag_settings.init()
    rag_db.init_vector_db()
    rag_updaters.update_llama_index_documents(use_saved_embeddings=True)

def get_query_engine():
    vector_index = rag_engines.get_semantic_query_index()
    semantic_query_retriever = rag_engines.get_semantic_query_retriever_engine()
    sql_query_engine = rag_engines.get_sql_query_engine()

    vector_tool = QueryEngineTool.from_defaults(
        query_engine=semantic_query_retriever,
        description=(
            f"Useful for answering semantic questions about different blog posts"
        ),
    )
    
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating a natural language query into a SQL query over"
            " a table containing: blog posts and page views each blog post"
        ),
    )
    
    return rag_patches.MySQLAutoVectorQueryEngine(
        sql_tool,
        vector_tool,
    )

def process_query(query_engine, query_text):
    old_stdout = sys.stdout
    mystdout = io.StringIO()
    sys.stdout = mystdout
    
    try:
        response = query_engine.query(query_text)
        debug_output = mystdout.getvalue()

        debug_info = {
            'query_type': 'Unknown',
            'explanation': '',
            'sql_query': '',
            'sql_response': '',
            'transformed_query': '',
            'full_debug': debug_output
        }

        if "Querying SQL database:" in debug_output:
            debug_info['query_type'] = 'SQL'
            explanation_start = debug_output.find("Querying SQL database:") + len("Querying SQL database:")
            explanation_end = debug_output.find("\n", explanation_start)
            debug_info['explanation'] = debug_output[explanation_start:explanation_end].strip()
        elif "Querying other query engine:" in debug_output:
            debug_info['query_type'] = 'Vector'
            explanation_start = debug_output.find("Querying other query engine:") + len("Querying other query engine:")
            explanation_end = debug_output.find("\n", explanation_start)
            debug_info['explanation'] = debug_output[explanation_start:explanation_end].strip()

        if "SQL query:" in debug_output:
            sql_query_start = debug_output.find("SQL query:") + len("SQL query:")
            sql_query_end = debug_output.find("SQL response:", sql_query_start)
            if sql_query_end == -1:
                sql_query_end = len(debug_output)
            debug_info['sql_query'] = debug_output[sql_query_start:sql_query_end].strip()

        if "SQL response:" in debug_output:
            sql_response_start = debug_output.find("SQL response:") + len("SQL response:")
            sql_response_end = debug_output.find("Transformed query given SQL response:", sql_response_start)
            if sql_response_end == -1:
                sql_response_end = len(debug_output)
            debug_info['sql_response'] = debug_output[sql_response_start:sql_response_end].strip()
        
        return response, debug_info
    finally:
        sys.stdout = old_stdout