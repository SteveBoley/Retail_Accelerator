# Generated by Django 2.2.14 on 2023-05-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_userprofile_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.AddField(
            model_name='item',
            name='subcat',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='subcat_id',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
