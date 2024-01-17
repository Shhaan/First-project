# Generated by Django 4.2.7 on 2023-12-22 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0015_alter_orderitem_shipping_choice"),
    ]

    operations = [
        migrations.CreateModel(
            name="shipping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shipping_name", models.CharField(max_length=50)),
                ("shipping_price", models.IntegerField()),
                ("des", models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="shipping_choice",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="shipping_option",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userorder.shipping",
            ),
        ),
    ]
