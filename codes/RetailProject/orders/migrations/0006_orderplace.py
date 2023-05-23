# Generated by Django 4.1.7 on 2023-05-23 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_created=True)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.discountpackage')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.productcategory')),
            ],
        ),
    ]
