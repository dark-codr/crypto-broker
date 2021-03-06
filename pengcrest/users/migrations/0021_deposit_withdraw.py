# Generated by Django 3.2.12 on 2022-04-11 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_wallet_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('DASH', 'DASH')], default='BTC', max_length=16)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('FAILED', 'FAILED'), ('SUCCESS', 'SUCCESS')], default='PENDING', max_length=15)),
                ('amount', models.DecimalField(decimal_places=7, default=0.0, max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='withraw', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Withdraw History',
                'verbose_name_plural': 'Withdraw Histories',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC'), ('DASH', 'DASH')], default='BTC', max_length=16)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('FAILED', 'FAILED'), ('SUCCESS', 'SUCCESS')], default='PENDING', max_length=15)),
                ('amount', models.DecimalField(decimal_places=7, default=0.0, max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='depsit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deposit History',
                'verbose_name_plural': 'Deposit Histories',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
    ]
