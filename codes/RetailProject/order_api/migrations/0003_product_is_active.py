# Generated by Django 4.1.7 on 2023-07-03 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0002_alter_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
