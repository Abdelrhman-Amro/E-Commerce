# Generated by Django 5.1.6 on 2025-03-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_options_alter_seller_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='store_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
