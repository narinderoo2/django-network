# Generated by Django 4.1.3 on 2023-03-15 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_rename_device_id_chartdetails_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartdetails',
            name='modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 15, 8, 48, 29, 14150, tzinfo=datetime.timezone.utc)),
        ),
    ]