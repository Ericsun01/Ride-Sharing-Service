# Generated by Django 3.0.2 on 2020-02-07 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0012_auto_20200207_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
