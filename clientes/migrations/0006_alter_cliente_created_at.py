# Generated by Django 4.1.5 on 2024-11-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0005_alter_cliente_estatus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="created_at",
            field=models.DateTimeField(),
        ),
    ]
