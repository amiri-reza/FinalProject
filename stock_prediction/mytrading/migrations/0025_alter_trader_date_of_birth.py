# Generated by Django 4.1.6 on 2023-05-20 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mytrading", "0024_alter_trader_date_of_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trader",
            name="date_of_birth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 5, 20, 11, 35, 32, 391948, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]