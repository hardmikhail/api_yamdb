# Generated by Django 3.2 on 2023-04-29 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение'),
        ),
        migrations.AddField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre', verbose_name='Жанр'),
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='произведение'),
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(help_text='Пользователь, который оставил комментарий', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AddField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]
