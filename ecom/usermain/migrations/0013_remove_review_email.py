# Generated by Django 4.2.7 on 2023-12-17 09:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("usermain", "0012_alter_review_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="email",
        ),
    ]
