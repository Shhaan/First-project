# Generated by Django 4.2.7 on 2023-12-09 02:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usermain", "0008_delete_customtotpdevice"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="otp",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
