# Generated by Django 4.1.7 on 2023-05-23 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_discountpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Table name')),
                ('number_of_chair', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
