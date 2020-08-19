# Generated by Django 3.0.9 on 2020-08-19 01:07

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('payload', models.TextField(default='{}', verbose_name='payload')),
                ('scope', models.CharField(choices=[('profile', 'profile'), ('sheet', 'sheet'), ('record', 'record')], max_length=30, verbose_name='scope')),
                ('expire_at', models.DateTimeField(verbose_name='expire at')),
                ('usage', models.SmallIntegerField(default=0, verbose_name='usage')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
        ),
    ]
