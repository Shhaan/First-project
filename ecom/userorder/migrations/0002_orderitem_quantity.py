# Generated by Django 4.2.7 on 2023-12-18 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
