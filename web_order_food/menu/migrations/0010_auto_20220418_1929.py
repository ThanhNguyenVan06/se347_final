# Generated by Django 3.1 on 2022-04-18 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_cart_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 18, 19, 29, 21, 775)),
        ),
    ]
