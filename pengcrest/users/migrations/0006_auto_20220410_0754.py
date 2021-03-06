# Generated by Django 3.2.12 on 2022-04-10 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, help_text='eg: 018276475673', max_length=17),
        ),
        migrations.AddField(
            model_name='user',
            name='recommended_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid1, editable=False),
        ),
    ]
