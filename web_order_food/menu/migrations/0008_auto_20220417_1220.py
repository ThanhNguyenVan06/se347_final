# Generated by Django 3.1 on 2022-04-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_auto_20220417_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='active_bill',
        ),
        migrations.AddField(
            model_name='cart',
            name='active',
            field=models.IntegerField(choices=[(0, 'no'), (1, 'yes')], default=0),
        ),
    ]
