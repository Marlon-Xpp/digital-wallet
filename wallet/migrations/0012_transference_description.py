# Generated by Django 5.1.1 on 2024-09-28 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0011_transference_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='transference',
            name='description',
            field=models.CharField(default='', max_length=250),
        ),
    ]
