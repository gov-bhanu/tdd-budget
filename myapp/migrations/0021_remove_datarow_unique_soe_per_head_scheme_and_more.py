# Generated by Django 5.1.3 on 2024-11-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_remove_datarow_unique_soe_per_head_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='datarow',
            name='unique_soe_per_head_scheme',
        ),
        migrations.AddConstraint(
            model_name='datarow',
            constraint=models.UniqueConstraint(fields=('soe_name', 'head_name'), name='unique_soe_per_head'),
        ),
    ]