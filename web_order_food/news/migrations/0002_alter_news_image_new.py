# Generated by Django 4.0.3 on 2022-06-12 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image_new',
            field=models.TextField(),
        ),
    ]
