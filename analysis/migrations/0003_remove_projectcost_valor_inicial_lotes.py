# Generated by Django 4.1.5 on 2024-11-06 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0002_rename_precio_venta_lotes_projectcost_precio_por_m2"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projectcost",
            name="valor_inicial_lotes",
        ),
    ]
