# Generated by Django 4.1.3 on 2023-03-06 10:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('total_ram', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ChartDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('ram', models.CharField(max_length=200)),
                ('battery', models.CharField(max_length=200)),
                ('cpu', models.CharField(max_length=200)),
                ('modified', models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 6, 10, 21, 38, 404049, tzinfo=datetime.timezone.utc))),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.devicedetails')),
            ],
        ),
    ]
