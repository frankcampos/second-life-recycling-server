# Generated by Django 4.2.13 on 2024-07-13 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_life_recycling_api', '0002_categories_recyclable_items_shopping_cart_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=100)),
                ('vendor_address', models.CharField(max_length=100)),
            ],
        ),
    ]
