# Generated by Django 3.2.12 on 2022-04-09 12:17

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('mode', '0003_alter_currency_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('doc', tinymce.models.HTMLField(verbose_name='Agreement')),
            ],
            options={
                'verbose_name': 'Customer Agreement',
                'verbose_name_plural': 'Customer Agreements',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('doc', tinymce.models.HTMLField(verbose_name='Privacy')),
            ],
            options={
                'verbose_name': 'Privacy Statement',
                'verbose_name_plural': 'Privacy Statements',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('doc', tinymce.models.HTMLField(verbose_name='Return')),
            ],
            options={
                'verbose_name': 'Return Policy',
                'verbose_name_plural': 'Return Policies',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
    ]
