# Generated by Django 5.1.3 on 2024-12-18 21:27

import django_bleach.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_alter_comment_commenttext_alter_post_posttext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentText',
            field=django_bleach.models.BleachField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='postText',
            field=django_bleach.models.BleachField(),
        ),
    ]
