# Generated by Django 3.0.7 on 2020-06-14 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200614_1841'),
        ('notebooks', '0002_auto_20200614_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='record',
            name='seller',
        ),
        migrations.AddField(
            model_name='record',
            name='attendant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attendant', to='accounts.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='attended',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='attended', to='accounts.Profile'),
            preserve_default=False,
        ),
    ]