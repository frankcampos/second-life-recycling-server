# Generated by Django 4.1.3 on 2024-07-17 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('second_life_recycling_api', '0005_rename_user_id_recyclable_items_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopping_cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='shopping_cart',
            name='item_id',
        ),
        migrations.RemoveField(
            model_name='shopping_cart',
            name='price',
        ),
        migrations.RemoveField(
            model_name='shopping_cart',
            name='status',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_life_recycling_api.shopping_cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_life_recycling_api.recyclable_items')),
            ],
        ),
    ]