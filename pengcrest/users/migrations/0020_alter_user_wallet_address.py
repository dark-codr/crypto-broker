# Generated by Django 3.2.12 on 2022-04-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20220411_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
