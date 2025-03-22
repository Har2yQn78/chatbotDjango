from django.db import models

class QueryHistory(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    query_type = models.CharField(max_length=20, choices=[
        ('sql', 'SQL Query'),
        ('vector', 'Vector Query'),
        ('auto', 'Auto Query'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Query histories"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.query_text[:50]}... ({self.query_type})"