from django.urls import path
from . import views

urlpatterns = [
    path('ragui/', views.rag_ui, name='rag_ui'),
    path('query-rag/', views.query_rag, name='query_rag'),  
]