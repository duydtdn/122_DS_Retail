# Generated by Django 4.1.7 on 2023-08-08 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0014_customuser_device_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
