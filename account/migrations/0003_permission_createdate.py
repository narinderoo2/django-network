# Generated by Django 4.1.3 on 2023-03-17 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_role_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='createDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 17, 10, 11, 36, 728081, tzinfo=datetime.timezone.utc)),
        ),
    ]
