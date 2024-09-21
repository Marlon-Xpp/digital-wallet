# Generated by Django 5.1.1 on 2024-09-21 02:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='description',
            field=models.CharField(default='', max_length=250),
        ),
    ]
