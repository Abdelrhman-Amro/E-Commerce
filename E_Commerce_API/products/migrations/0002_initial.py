# Generated by Django 5.1.6 on 2025-03-12 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.store'),
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='products.product'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='product_name_c4c985_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['store_id'], name='product_store_i_05b736_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category_id'], name='product_categor_5f9fc7_idx'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(condition=models.Q(('price__gt', 0)), name='price_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(condition=models.Q(('stock_quantity__gte', 0), ('stock_quantity__lte', 9999)), name='stock_quantity_gte_0'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['product', 'rating'], name='review_product_a2d083_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['is_verified_purchase'], name='review_is_veri_943583_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['reviewer'], name='review_reviewe_cff1ab_idx'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(condition=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range_1_to_5'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('product', 'reviewer')},
        ),
    ]
