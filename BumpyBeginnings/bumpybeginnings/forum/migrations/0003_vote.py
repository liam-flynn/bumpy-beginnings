# Generated by Django 5.1.3 on 2024-11-30 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_comment_score'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], max_length=10)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='forum.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
    ]
