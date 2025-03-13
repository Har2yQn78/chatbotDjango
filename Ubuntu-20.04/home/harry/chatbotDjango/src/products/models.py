from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from pgvector.django import VectorField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

EMBEDDING_MODEL="mistral-embed"
EMEDDING_LENGTH=1024


class Embedding(models.Model):
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    object_id = models.PositiveIntegerField()  # Added parentheses here
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

# ... rest of the file remains unchanged ...