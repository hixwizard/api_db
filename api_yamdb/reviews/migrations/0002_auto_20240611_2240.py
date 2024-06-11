# Generated by Django 3.2 on 2024-06-11 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='reviews',
            name='author_and_text',
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.reviews', verbose_name='ID отзыва'),
        ),
        migrations.AddConstraint(
            model_name='reviews',
            constraint=models.UniqueConstraint(fields=('author',), name='unique'),
        ),
    ]
