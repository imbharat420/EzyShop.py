# Generated by Django 4.2.1 on 2023-05-04 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
    ]