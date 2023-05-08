# Generated by Django 4.2.1 on 2023-05-08 07:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]