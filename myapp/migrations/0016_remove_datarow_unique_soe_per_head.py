# Generated by Django 5.1.3 on 2024-11-21 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_remove_datarow_unique_department_code_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='datarow',
            name='unique_soe_per_head',
        ),
    ]