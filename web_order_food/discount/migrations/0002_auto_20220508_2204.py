# Generated by Django 3.1 on 2022-05-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='discounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image_discount', models.ImageField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='news',
        ),
    ]
