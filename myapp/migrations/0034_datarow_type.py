# Generated by Django 5.1.3 on 2024-11-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_alter_datarow_scheme_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarow',
            name='type',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]