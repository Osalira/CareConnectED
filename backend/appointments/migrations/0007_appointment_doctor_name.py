# Generated by Django 5.1.4 on 2024-12-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_appointment_checked_in_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctor_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
