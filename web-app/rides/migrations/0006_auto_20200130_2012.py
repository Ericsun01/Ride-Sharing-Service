# Generated by Django 3.0.2 on 2020-01-30 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0005_auto_20200130_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='user',
            field=models.IntegerField(default=0),
        ),
    ]
