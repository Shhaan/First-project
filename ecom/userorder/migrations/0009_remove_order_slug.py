# Generated by Django 4.2.7 on 2023-12-21 17:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0008_order_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="slug",
        ),
    ]
