# Generated by Django 5.1.4 on 2024-12-08 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_alter_appointment_scheduled_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='checked_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='checked_out_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='state',
            field=models.CharField(choices=[('triage', 'Triage'), ('checked-in', 'Checked In'), ('checked-out', 'Checked Out')], default='triage', max_length=20),
        ),
    ]
