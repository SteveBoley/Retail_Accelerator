# Generated by Django 2.2.14 on 2023-05-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='customer_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]