# Generated by Django 3.2.12 on 2022-04-11 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_user_has_toped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dash_address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='eth_address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='ltc_address',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
