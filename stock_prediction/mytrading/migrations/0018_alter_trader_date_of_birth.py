# Generated by Django 4.2 on 2023-05-04 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mytrading", "0017_alter_trader_date_of_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trader",
            name="date_of_birth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 5, 4, 16, 40, 53, 357057, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
