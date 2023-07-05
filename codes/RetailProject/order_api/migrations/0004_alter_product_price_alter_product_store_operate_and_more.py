# Generated by Django 4.1.7 on 2023-07-06 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0003_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='store_operate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_api.store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=512),
        ),
    ]
