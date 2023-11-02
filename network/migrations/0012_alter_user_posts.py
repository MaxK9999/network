# Generated by Django 4.2.6 on 2023-11-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_user_followers_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='posted_by', to='network.post'),
        ),
    ]