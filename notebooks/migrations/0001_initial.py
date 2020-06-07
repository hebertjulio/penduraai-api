# Generated by Django 3.0.7 on 2020-06-06 23:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRecord',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('authorized', models.BooleanField(default=True, verbose_name='authorized')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_creditor', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_debtor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'customer record',
                'verbose_name_plural': 'customer records',
                'unique_together': {('creditor', 'debtor')},
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='note')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='value')),
                ('operation', models.CharField(choices=[('payment', 'payment'), ('debt', 'debt')], db_index=True, max_length=30, verbose_name='operation')),
                ('strikethrough', models.BooleanField(default=False, verbose_name='strikethrough')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_buyer', to='accounts.Profile')),
                ('customer_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_record', to='notebooks.CustomerRecord')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_seller', to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'record',
                'verbose_name_plural': 'records',
            },
        ),
    ]
