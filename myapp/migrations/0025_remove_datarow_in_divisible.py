# Generated by Django 5.1.3 on 2024-11-23 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_rename_divisible_datarow_in_divisible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datarow',
            name='in_divisible',
        ),
    ]