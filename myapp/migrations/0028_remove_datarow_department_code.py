# Generated by Django 5.1.3 on 2024-11-25 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_datarow_divisible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datarow',
            name='department_code',
        ),
    ]