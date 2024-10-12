# Generated by Django 5.1.1 on 2024-10-08 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wallet", "0013_userpayment_delete_transference"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transference",
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
                ("name", models.CharField(max_length=250)),
                ("lastname", models.CharField(max_length=250)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("username", models.CharField(max_length=250)),
                ("description", models.CharField(default="", max_length=250)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "type_transference",
                    models.CharField(
                        choices=[("SEND", "send"), ("REQUEST", "request")],
                        max_length=100,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "idWallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wallet.wallet"
                    ),
                ),
            ],
        ),
    ]
