# Generated by Django 3.2.12 on 2022-04-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20220411_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dash_address',
            field=models.CharField(blank=True, max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='eth_address',
            field=models.CharField(blank=True, max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ltc_address',
            field=models.CharField(blank=True, max_length=250, unique=True),
        ),
    ]
