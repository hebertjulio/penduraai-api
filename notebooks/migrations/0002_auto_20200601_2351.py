# Generated by Django 3.0.6 on 2020-06-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='authorized',
            field=models.BooleanField(default=True, verbose_name='authorized'),
        ),
    ]