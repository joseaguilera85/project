# Generated by Django 4.1.5 on 2024-11-10 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0004_project_end_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="end_date",
        ),
    ]
