# Generated by Django 5.1.6 on 2025-03-13 23:28

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('role', models.CharField(choices=[('seller', 'Seller'), ('customer', 'Customer')], default='customer', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'customuser',
                'verbose_name_plural': 'customusers',
                'db_table': 'customuser',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store_name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'store',
                'verbose_name_plural': 'stores',
                'db_table': 'store',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('street_address', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('special_mark', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
                ('store', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='users.store')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'db_table': 'address',
            },
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['email'], name='customuser_email_f5e4ce_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['username'], name='customuser_usernam_2f899c_idx'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['store_name'], name='store_store_n_fd868d_idx'),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['user'], name='address_user_id_598b7f_idx'),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['store'], name='address_store_i_0622ca_idx'),
        ),
    ]
