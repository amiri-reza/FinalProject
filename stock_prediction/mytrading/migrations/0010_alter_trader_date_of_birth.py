# Generated by Django 4.1.6 on 2023-04-26 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mytrading", "0009_alter_trader_date_of_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trader",
            name="date_of_birth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 4, 26, 14, 49, 28, 225756, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
