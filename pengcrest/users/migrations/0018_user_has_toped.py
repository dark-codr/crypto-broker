# Generated by Django 3.2.12 on 2022-04-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20220411_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_toped',
            field=models.BooleanField(default=False),
        ),
    ]