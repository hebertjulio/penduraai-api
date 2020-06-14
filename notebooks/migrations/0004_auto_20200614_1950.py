# Generated by Django 3.0.7 on 2020-06-14 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0003_auto_20200614_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Designates whether this record should be treated as deleted. Select this instead of deleting record.', verbose_name='deleted status'),
        ),
    ]
