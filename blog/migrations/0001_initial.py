# Generated by Django 5.1.2 on 2024-10-15 20:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Адреса URL')),
                ('body', models.TextField(blank=True, verbose_name='Зміст')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публікації')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата змінення')),
                ('status', models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2, verbose_name='Статус посту')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'db_table': 'posts',
                'ordering': ['-publish'],
                'indexes': [models.Index(fields=['-publish'], name='posts_publish_42cf87_idx')],
            },
        ),
    ]
