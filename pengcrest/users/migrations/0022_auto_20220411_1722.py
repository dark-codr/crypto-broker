# Generated by Django 3.2.12 on 2022-04-11 21:22

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_deposit_withdraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('DASH', 'DASH')], default='BTC', max_length=16)),
                ('wallet', models.CharField(blank=True, max_length=250)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Wallet Address',
                'verbose_name_plural': 'Wallet Addresses',
                'ordering': ['-modified'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='withdraw',
            name='wallet',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
