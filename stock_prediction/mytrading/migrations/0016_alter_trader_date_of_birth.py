# Generated by Django 4.2 on 2023-05-02 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mytrading", "0015_alter_trader_date_of_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trader",
            name="date_of_birth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 5, 2, 12, 18, 34, 563971, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]