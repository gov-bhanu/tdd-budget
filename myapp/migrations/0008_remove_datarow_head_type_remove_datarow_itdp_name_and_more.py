# Generated by Django 5.1.3 on 2024-11-20 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_datarow_unique_id_datarow_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datarow',
            name='head_type',
        ),
        migrations.RemoveField(
            model_name='datarow',
            name='itdp_name',
        ),
        migrations.AddField(
            model_name='datarow',
            name='bharmaur',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datarow',
            name='kinnaur',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datarow',
            name='lahaul',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datarow',
            name='pangi',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datarow',
            name='spiti',
            field=models.FloatField(blank=True, null=True),
        ),
    ]