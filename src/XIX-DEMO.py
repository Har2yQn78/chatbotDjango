#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setup

setup.init_django()


# In[2]:


from rag import (
    db as rag_db, 
    engines as rag_engines,
    settings as rag_settings, 
    updaters as rag_updaters,
    patches as rag_patches,
)


# In[3]:


from typing import Optional, Union
from sqlalchemy import create_engine, text


# In[4]:


rag_settings.init()
rag_db.init_vector_db()
rag_updaters.update_llama_index_documents(use_saved_embeddings=True)


# In[5]:


vector_index = rag_engines.get_semantic_query_index()
semantic_query_retriever = rag_engines.get_semantic_query_retriever_engine()
sql_query_engine = rag_engines.get_sql_query_engine()


# In[6]:


print(rag_settings.VECTOR_DB_NAME, rag_settings.VECTOR_DB_TABLE_NAME)


# In[7]:


from llama_index.core.tools import QueryEngineTool

vector_tool = QueryEngineTool.from_defaults(
    query_engine=semantic_query_retriever,
    description=(
        f"Useful for answering semantic questions about different blog posts"
    ),
)


# In[8]:


sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description=(
        "Useful for translating a natural language query into a SQL query over"
        " a table containing: blog posts and page views each blog post"
    ),
)


# In[9]:


query_engine = rag_patches.MySQLAutoVectorQueryEngine(
    sql_tool, 
    vector_tool,
)


# In[10]:


response = query_engine.query(
    "What do you make?"
)


# In[11]:


response.response


# In[12]:


response = query_engine.query(
    "Are are the top 5 most viewed blog posts? What keywords do their content have?"
)


# In[13]:


from IPython.display import Markdown, display

display(Markdown(response.response))


# In[14]:


response = query_engine.query(
    "What are the top 5 least viewed blog posts in the year 2024 to 2025?"
)
print(response.response)


# In[15]:


display(Markdown(response.response))


# In[ ]:




