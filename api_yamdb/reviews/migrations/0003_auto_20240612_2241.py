# Generated by Django 3.2 on 2024-06-12 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='title',
            new_name='title_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title',
            new_name='title_id',
        ),
    ]
