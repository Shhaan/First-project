# Generated by Django 4.2.7 on 2023-12-15 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("adminhome", "0012_alter_brand_brand_name_alter_category_category_name"),
        ("usermain", "0011_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_review",
                to="adminhome.products",
            ),
        ),
    ]
