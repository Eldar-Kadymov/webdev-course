# Generated by Django 4.2.2 on 2023-08-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_task_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
