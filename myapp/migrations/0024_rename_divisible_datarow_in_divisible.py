# Generated by Django 5.1.3 on 2024-11-23 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_datarow_divisible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datarow',
            old_name='divisible',
            new_name='in_divisible',
        ),
    ]