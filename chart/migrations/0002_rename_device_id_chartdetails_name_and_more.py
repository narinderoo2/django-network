# Generated by Django 4.1.3 on 2023-03-06 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chartdetails',
            old_name='device_id',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='chartdetails',
            name='modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 6, 11, 6, 15, 619236, tzinfo=datetime.timezone.utc)),
        ),
    ]