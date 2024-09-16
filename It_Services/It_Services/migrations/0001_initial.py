# Generated by Django 5.0 on 2024-08-20 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=100)),
                ('payment_terms', models.TextField()),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_package', models.CharField(max_length=100)),
                ('service_tax', models.DecimalField(decimal_places=2, max_digits=5)),
                ('service_image', models.ImageField(upload_to='services/')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('check_me_out', models.BooleanField(default=False)),
            ],
        ),
    ]
