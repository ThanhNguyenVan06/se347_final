# Generated by Django 3.1 on 2022-04-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('id_foods', models.TextField()),
                ('bill_code', models.CharField(max_length=100, null=True)),
                ('active', models.IntegerField(choices=[(0, 'no'), (1, 'yes')], default=0)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('name_food', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=200)),
                ('active', models.IntegerField(choices=[(0, 'no serve'), (1, 'serve')], default=1)),
            ],
        ),
    ]
