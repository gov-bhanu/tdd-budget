# Generated by Django 5.1.3 on 2024-11-26 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_remove_datarow_department_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarow',
            name='agreed_by_fd',
            field=models.FloatField(blank=True, null=True),
        ),
    ]