# Generated by Django 5.1.4 on 2024-12-08 03:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_patient_remove_appointment_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='scheduled_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]