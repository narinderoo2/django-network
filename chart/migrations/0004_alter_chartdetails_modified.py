# Generated by Django 4.1.3 on 2023-03-27 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0003_alter_chartdetails_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartdetails',
            name='modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 27, 18, 7, 57, 206756)),
        ),
    ]
