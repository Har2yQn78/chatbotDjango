from django.contrib import admin

from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    readonly_fields = ['timestamp']

admin.site.register(BlogPost, BlogPostAdmin)