# Generated by Django 4.1.7 on 2023-07-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0009_orderplace_pay_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(default='', max_length=10, null=True),
        ),
    ]