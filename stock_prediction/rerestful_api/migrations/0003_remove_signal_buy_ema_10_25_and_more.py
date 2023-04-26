# Generated by Django 4.1.6 on 2023-04-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rerestful_api", "0002_signal_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="signal",
            name="buy_ema_10_25",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_ema_10_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_ema_25_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_emas",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_sma_10_25",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_sma_10_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_sma_25_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="buy_smas",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_ema_10_25",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_ema_10_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_ema_25_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_emas",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_sma_10_25",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_sma_10_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_sma_25_50",
        ),
        migrations.RemoveField(
            model_name="signal",
            name="sell_smas",
        ),
        migrations.AddField(
            model_name="signal",
            name="signal_type",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="signal",
            name="value",
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]