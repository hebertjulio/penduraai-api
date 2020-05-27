# Generated by Django 3.0.6 on 2020-05-27 17:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='value')),
                ('operation', models.CharField(choices=[('payment', 'payment'), ('debt', 'debt')], db_index=True, max_length=30, verbose_name='operation')),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected')], db_index=True, max_length=30, verbose_name='status')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_buyer', to='accounts.Profile')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_creditor', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_debtor', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_seller', to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'record',
                'verbose_name_plural': 'records',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('authorized', models.BooleanField(verbose_name='authorized')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers_creditor', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers_debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
                'unique_together': {('creditor', 'debtor')},
            },
        ),
    ]
