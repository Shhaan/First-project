# Generated by Django 4.2.7 on 2023-12-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0008_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='status',
            field=models.CharField(choices=[('sale', 'Sale'), ('out of stock', 'Out of stock')], default='sale', max_length=20),
        ),
    ]
