# Generated by Django 4.2.5 on 2023-10-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='commented_by', to='network.comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='posts',
            field=models.ManyToManyField(related_name='posted_by', to='network.post'),
        ),
    ]