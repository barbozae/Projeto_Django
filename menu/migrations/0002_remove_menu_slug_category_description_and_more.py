# Generated by Django 5.1.5 on 2025-03-24 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
