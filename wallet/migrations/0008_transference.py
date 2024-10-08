# Generated by Django 5.1.1 on 2024-09-27 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_delete_transference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('lastname', models.CharField(max_length=250)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('type_transference', models.CharField(choices=[('SEND', 'send'), ('REQUEST', 'request')], max_length=100)),
                ('idWallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.wallet')),
            ],
        ),
    ]
