# Generated by Django 4.2.7 on 2023-12-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0006_orderitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
