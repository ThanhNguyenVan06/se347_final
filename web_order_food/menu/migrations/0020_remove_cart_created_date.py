# Generated by Django 3.1 on 2022-04-18 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0019_auto_20220418_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_date',
        ),
    ]
