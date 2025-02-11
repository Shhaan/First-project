# Generated by Django 4.2.7 on 2023-12-25 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0022_coupon_order_coupon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userorder.coupon",
            ),
        ),
    ]
