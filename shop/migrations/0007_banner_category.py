# Generated by Django 4.2.1 on 2023-05-08 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('shop', '0006_banner_created_date_banner_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
        ),
    ]
