# Generated by Django 3.2.12 on 2022-04-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20220411_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_investment',
            field=models.BooleanField(default=False),
        ),
    ]
