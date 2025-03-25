from rag import (
    db as rag_db,
    engines as rag_engines,
    settings as rag_settings,
    updaters as rag_updaters,
    sync as rag_sync, 
    patches as rag_patches,
)
from llama_index.core.tools import QueryEngineTool
import io
import sys

def initialize_rag():
    rag_settings.init()
    rag_db.init_vector_db()
    rag_sync.full_sync()

def get_query_engine():
    product_query_engine = rag_engines.get_semantic_query_engine("Product")
    employee_query_engine = rag_engines.get_semantic_query_engine("Employee")
    inventory_query_engine = rag_engines.get_semantic_query_engine("InventoryItem")
    ProductType_query_engine = rag_engines.get_semantic_query_engine("ProductType")
    sql_query_engine = rag_engines.get_sql_query_engine()

    product_tool = QueryEngineTool.from_defaults(
        query_engine=product_query_engine,
        description=(
            "Useful for answering semantic questions about coffee shop products, "
            "including ingredients, pricing, and availability"
        ),
    )

    employee_tool = QueryEngineTool.from_defaults(
        query_engine=employee_query_engine,
        description=(
             "Useful for questions about staff members, their roles, schedules, "
            "or employment details"
        ),
    )

    inventory_tool = QueryEngineTool.from_defaults(
        query_engine=inventory_query_engine,
        description=(
             "Useful for questions about stock levels, inventory items, "
            "or supply requirements"
        ),
    )

    
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating natural language queries into SQL over tables containing: "
            "EmployeeRole, Employee, ProductType, Product, InventoryItem, ProductInventoryRequirement"
        ),
    )
    
    return rag_patches.MySQLAutoVectorQueryEngine(
        sql_tool,
        product_tool,
        employee_tool,
        inventory_tool,
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