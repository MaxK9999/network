# Generated by Django 4.2.5 on 2023-10-25 11:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_id_alter_user_id_comment_post_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_comments', to='network.comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
