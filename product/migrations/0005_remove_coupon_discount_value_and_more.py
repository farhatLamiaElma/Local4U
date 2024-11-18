# Generated by Django 5.1.3 on 2024-11-18 03:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_coupon_alter_product_farmer_discount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount_value',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='active',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='discount_value',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='product',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.discount'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='used_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discount',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='product.category'),
        ),
        migrations.AddField(
            model_name='discount',
            name='code',
            field=models.CharField(default='DEFAULT_CODE', max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Discount percentage (e.g., 10.00 for 10%)', max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='discounts', to='product.product'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
