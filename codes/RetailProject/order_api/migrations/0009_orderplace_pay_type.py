# Generated by Django 4.1.7 on 2023-07-13 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0008_alter_discountpackage_gift_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplace',
            name='pay_type',
            field=models.CharField(choices=[('online_pay', 'Online pay'), ('ship_cod', 'Ship COD'), ('onboard', 'Onboard')], default='onboard', max_length=20),
        ),
    ]
