# Generated by Django 5.1.3 on 2024-11-26 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_remove_cliente_estatus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oportunidad',
            name='descripcion',
        ),
    ]
