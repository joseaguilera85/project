# Generated by Django 4.1.5 on 2024-11-13 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0002_rename_id_cliente_id_client"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cliente",
            old_name="id_client",
            new_name="id_cliente",
        ),
    ]
