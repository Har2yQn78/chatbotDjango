from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from pgvector.django import VectorField

EMBEDDING_MODEL="mistral-embed"
EMEDDING_LENGTH=1024


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    _content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    can_delete = models.BooleanField(default=False, help_text="Use in jupyter notebooks")

    def get_embedding_text_raw(self):
        return self.content