# Generated by Django 5.1.1 on 2024-09-27 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_alter_wallet_user_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transference',
        ),
    ]
