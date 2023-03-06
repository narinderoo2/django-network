# Generated by Django 4.1.3 on 2023-03-06 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('created_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('createdBy', models.CharField(max_length=50, null=True)),
                ('countryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='region.countryname')),
            ],
        ),
        migrations.CreateModel(
            name='CityName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country', to='region.countryname')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='region.statename')),
            ],
        ),
    ]
