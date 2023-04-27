# Generated by Django 4.2 on 2023-04-27 14:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rerestful_api', '0003_remove_signal_buy_ema_10_25_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='date',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='signal_type',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='value',
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_ema_10_25',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_ema_10_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_ema_25_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_emas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_sma_10_25',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_sma_10_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_sma_25_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='buy_smas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_ema_10_25',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_ema_10_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_ema_25_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_emas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_sma_10_25',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_sma_10_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_sma_25_50',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='signal',
            name='sell_smas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None),
        ),
    ]