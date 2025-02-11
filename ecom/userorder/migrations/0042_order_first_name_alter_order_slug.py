# Generated by Django 4.2.7 on 2024-01-10 19:19

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0041_alter_order_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="first_name",
            field=models.CharField(default="afad", max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False, populate_from="first_name", unique=True
            ),
        ),
    ]
