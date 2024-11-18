# Generated by Django 5.1.3 on 2024-11-18 03:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_farmer_location_remove_farmer_name'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        migrations.AlterField(
            model_name='product',
            name='farmer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.farmer'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='DEFAULT_CODE', max_length=20, unique=True)),
                ('discount_type', models.CharField(choices=[('promotional', 'Promotional'), ('seasonal', 'Seasonal')], max_length=20)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, help_text='Discount percentage (e.g., 10.00 for 10%)', max_digits=5, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='product.category')),
                ('products', models.ManyToManyField(blank=True, related_name='discounts', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('used_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('discount', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.discount')),
            ],
        ),
    ]