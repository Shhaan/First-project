# Generated by Django 4.2.7 on 2023-12-18 13:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("adminhome", "0012_alter_brand_brand_name_alter_category_category_name"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Order",
        ),
    ]
