# Generated by Django 4.1.5 on 2024-11-13 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("clientes", "0003_rename_id_client_cliente_id_cliente"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_clientes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]