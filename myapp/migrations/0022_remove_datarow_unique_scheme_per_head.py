# Generated by Django 5.1.3 on 2024-11-21 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_remove_datarow_unique_soe_per_head_scheme_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='datarow',
            name='unique_scheme_per_head',
        ),
    ]