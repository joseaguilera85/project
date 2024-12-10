# Generated by Django 4.1.5 on 2024-12-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0013_apartment_plano"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="apartment",
            name="plano",
        ),
        migrations.AddField(
            model_name="project",
            name="plano",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/apartments/plano/"
            ),
        ),
    ]
