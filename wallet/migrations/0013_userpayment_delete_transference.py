# Generated by Django 5.1.1 on 2024-10-08 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0012_transference_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_bool", models.BooleanField(default=False)),
                ("stripe_checkout_id", models.CharField(max_length=500)),
                (
                    "app_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wallet.wallet"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Transference",
        ),
    ]
