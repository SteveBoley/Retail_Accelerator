# Generated by Django 2.2.14 on 2023-05-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230501_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dummy_variable',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('S', 'sale'), ('N', 'new'), ('P', 'promotion')], max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.CharField(max_length=100),
        ),
    ]