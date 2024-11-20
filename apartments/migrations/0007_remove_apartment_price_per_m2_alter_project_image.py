# Generated by Django 4.1.5 on 2024-11-18 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0006_project_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="apartment",
            name="price_per_m2",
        ),
        migrations.AlterField(
            model_name="project",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/apartments/"
            ),
        ),
    ]