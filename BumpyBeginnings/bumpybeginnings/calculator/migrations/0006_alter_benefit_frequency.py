# Generated by Django 5.1.3 on 2025-02-13 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0005_benefit_dependent_benefits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='frequency',
            field=models.CharField(choices=[('once', 'Once'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('annually', 'Annually')], default='monthly', max_length=20),
        ),
    ]
