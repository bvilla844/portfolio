# Generated by Django 5.1.7 on 2025-03-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=20),
        ),
    ]
