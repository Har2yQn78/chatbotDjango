from django.shortcuts import render
from django.http import JsonResponse
from IPython.display import Markdown

from rag import (
    db as rag_db, 
    engines as rag_engines,
    settings as rag_settings, 
    updaters as rag_updaters,
    patches as rag_patches,
)
from llama_index.core.tools import QueryEngineTool

def initialize_rag():
    """Initialize RAG components"""
    rag_settings.init()
    rag_db.init_vector_db()
    rag_updaters.update_llama_index_documents(use_saved_embeddings=True)
    
    # Create query engines
    vector_index = rag_engines.get_semantic_query_index()
    semantic_query_retriever = rag_engines.get_semantic_query_retriever_engine()
    sql_query_engine = rag_engines.get_sql_query_engine()
    
    # Create tools
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=semantic_query_retriever,
        description="Useful for answering semantic questions about different blog posts"
    )
    
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating a natural language query into a SQL query over"
            " a table containing: blog posts and page views each blog post"
        ),
    )
    
    # Create combined query engine
    query_engine = rag_patches.MySQLAutoVectorQueryEngine(
        sql_tool, 
        vector_tool,
    )
    
    return query_engine

def rag_ui(request):
    """Render the RAG UI page"""
    return render(request, 'ragui/index.html')

def query_rag(request):
    """Handle AJAX query requests"""
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if not query:
            return JsonResponse({'error': 'No query provided'}, status=400)
        
        try:
            # Initialize RAG components
            query_engine = initialize_rag()
            
            # Execute query
            response = query_engine.query(query)
            
            # Return response
            return JsonResponse({
                'response': response.response,
                'success': True
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'success': False
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)