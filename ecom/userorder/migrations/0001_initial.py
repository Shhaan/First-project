# Generated by Django 4.2.7 on 2023-12-18 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminhome', '0013_delete_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('postal_code', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField()),
                ('country', models.CharField(max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('paid_amount', models.BigIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userorder.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminhome.products')),
            ],
        ),
    ]
