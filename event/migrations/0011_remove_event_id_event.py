# Generated by Django 4.2.1 on 2023-07-01 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_event_id_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='id_event',
        ),
    ]
