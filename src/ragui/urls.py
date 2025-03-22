from django.urls import path
from . import views

app_name = 'ragui'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('top-posts/', views.TopPostsView.as_view(), name='top_posts'),
]