# Generated by Django 3.0.2 on 2020-02-07 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0008_auto_20200207_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='_id',
            new_name='ride_id',
        ),
    ]
