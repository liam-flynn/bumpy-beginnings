# Generated by Django 5.1.3 on 2025-01-21 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PregnancyDevelopmentMilestone',
            fields=[
                ('week', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='milestone_images/')),
            ],
        ),
    ]
