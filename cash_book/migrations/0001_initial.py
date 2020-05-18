# Generated by Django 3.0.6 on 2020-05-18 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='value')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('done', 'done')], db_index=True, max_length=30, verbose_name='status')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditor', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
    ]
