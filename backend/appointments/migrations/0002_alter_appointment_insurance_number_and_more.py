# Generated by Django 5.1.3 on 2024-11-12 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='insurance_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='severity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
