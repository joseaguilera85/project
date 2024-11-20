# Generated by Django 4.1.5 on 2024-11-19 03:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0008_alter_cliente_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="interaction_status",
            field=models.CharField(
                choices=[
                    ("Recent", "Recent"),
                    ("Stale", "Stale"),
                    ("No Interaction", "No Interaction"),
                ],
                default="No Interaction",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="cliente",
            name="last_interaction",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]