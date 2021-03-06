# Generated by Django 2.1.7 on 2019-03-09 12:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import yukuz_oauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_created=True, auto_now=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(default='935852415', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(code='invalid phone number', message='Phone number should be numbers only', regex='^[0-9]*$')], verbose_name='Phone number')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
            },
            managers=[
                ('objects', yukuz_oauth.models.UBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='person', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ssn', models.PositiveIntegerField(unique=True, verbose_name='SSN')),
                ('first_name', models.CharField(default='', max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=50, verbose_name='Last Name')),
                ('email', models.CharField(blank=True, default='', max_length=50, verbose_name='e-mail')),
                ('image', models.ImageField(default='image/def_user', upload_to='images/users', verbose_name='image')),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='uuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='uuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='driver', serialize=False, to='yukuz_oauth.Person')),
                ('description', models.TextField(max_length=500, verbose_name='About driver')),
                ('driver_license', models.ImageField(upload_to='licenses/')),
                ('is_active', models.BooleanField(default=True)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
