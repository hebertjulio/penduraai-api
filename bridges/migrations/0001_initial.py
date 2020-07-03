# Generated by Django 3.0.8 on 2020-07-03 13:36

from django.conf import settings
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
            name='Transaction',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('scope', models.CharField(max_length=30, verbose_name='scope')),
                ('data', models.TextField(blank=True, verbose_name='data')),
                ('expire_at', models.DateTimeField(verbose_name='expire at')),
                ('status', models.CharField(choices=[('not_used', 'not used'), ('used', 'used'), ('discarded', 'discarded')], db_index=True, default='not_used', max_length=30, verbose_name='status')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiletransactions', to='accounts.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usertransactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
    ]
