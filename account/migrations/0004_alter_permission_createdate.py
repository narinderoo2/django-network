# Generated by Django 4.1.3 on 2023-03-17 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_permission_createdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='createDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]