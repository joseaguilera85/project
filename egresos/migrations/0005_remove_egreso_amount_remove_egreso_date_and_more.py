# Generated by Django 4.1.5 on 2024-11-13 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("egresos", "0004_remove_egreso_purchase_order_item_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="egreso",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="egreso",
            name="date",
        ),
        migrations.RemoveField(
            model_name="egreso",
            name="description",
        ),
    ]
