# Generated by Django 5.1.6 on 2025-03-24 18:38

import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffeshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeerole',
            name='embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=1024, null=True),
        ),
    ]
