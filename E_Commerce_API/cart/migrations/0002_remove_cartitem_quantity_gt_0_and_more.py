# Generated by Django 5.1.6 on 2025-03-06 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cartitem',
            name='quantity_gt_0',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='CartID',
            new_name='cart_id',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='UserID',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='CartID',
            new_name='cart_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='CartItemID',
            new_name='cart_item_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='ProductID',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='Quantity',
            new_name='quantity',
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.CheckConstraint(condition=models.Q(('quantity__gt', 0)), name='quantity_gt_0'),
        ),
    ]
