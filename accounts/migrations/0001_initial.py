# Generated by Django 3.0.9 on 2020-08-16 18:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('pin', models.CharField(db_index=True, max_length=4, validators=[django.core.validators.RegexValidator('\\d{4}')], verbose_name='pin')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this profile should be treated as active. Unselect this instead of deleting profile.', verbose_name='active status')),
                ('role', models.CharField(choices=[('owner', 'owner'), ('manager', 'manager'), ('attendant', 'attendant'), ('guest', 'guest')], db_index=True, max_length=30, verbose_name='role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
