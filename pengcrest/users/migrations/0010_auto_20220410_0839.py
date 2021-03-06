# Generated by Django 3.2.12 on 2022-04-10 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='kycverify',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='kycverify',
            name='id_type',
            field=models.CharField(blank=True, choices=[('PASSPORT', 'PASSPORT'), ('ID_CARD', 'ID CARD'), ('DRIVERS_LICENSE', 'DRIVERS LICENSE')], default='PASSPORT', max_length=15, null=True),
        ),
    ]
