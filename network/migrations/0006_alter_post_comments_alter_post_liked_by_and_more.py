# Generated by Django 4.2.5 on 2023-10-27 08:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_likes_post_liked_by_remove_user_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='post_comments', to='network.comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liking_users', to='network.post'),
        ),
    ]
