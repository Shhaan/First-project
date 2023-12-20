# Generated by Django 4.2.7 on 2023-12-12 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0010_alter_products_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
