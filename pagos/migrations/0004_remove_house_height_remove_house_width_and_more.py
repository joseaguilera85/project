# Generated by Django 5.1.3 on 2024-11-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0003_alter_house_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='height',
        ),
        migrations.RemoveField(
            model_name='house',
            name='width',
        ),
        migrations.RemoveField(
            model_name='house',
            name='x',
        ),
        migrations.RemoveField(
            model_name='house',
            name='y',
        ),
        migrations.AddField(
            model_name='house',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='points',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='house',
            name='color',
            field=models.CharField(max_length=7),
        ),
    ]
