# Generated by Django 2.2.14 on 2023-05-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20230501_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('FSHN0MC001', 'Men'), ('FSHN0MC002', 'Women'), ('FSHN0MC003', 'Kids'), ('FSHN0MC004', 'Beauty & Personal Care')], max_length=100),
        ),
    ]
