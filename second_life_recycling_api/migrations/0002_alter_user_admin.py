# Generated by Django 4.1.3 on 2024-07-31 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_life_recycling_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]