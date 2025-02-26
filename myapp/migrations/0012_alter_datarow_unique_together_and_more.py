# Generated by Django 5.1.3 on 2024-11-21 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_datarow_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datarow',
            unique_together={('department_code', 'department_name')},
        ),
        migrations.AddConstraint(
            model_name='datarow',
            constraint=models.UniqueConstraint(fields=('head_name', 'department_name'), name='unique_head_name_per_department'),
        ),
    ]
