# Generated by Django 3.0.6 on 2020-05-21 12:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='value')),
                ('type', models.CharField(choices=[('payment', 'payment'), ('debt', 'debt')], db_index=True, max_length=30, verbose_name='type')),
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
            name='Whitelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('authorized', 'authorized'), ('unauthorized', 'unauthorized')], db_index=True, max_length=30, verbose_name='status')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whitelists_creditor', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whitelists_debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'whitelist',
                'verbose_name_plural': 'whitelists',
                'unique_together': {('creditor', 'debtor')},
            },
        ),
    ]
