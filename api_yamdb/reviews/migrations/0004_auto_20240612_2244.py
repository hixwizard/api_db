# Generated by Django 3.2 on 2024-06-12 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20240612_2241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='title_id',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title_id',
            new_name='title',
        ),
    ]
