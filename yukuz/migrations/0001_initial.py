# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15)),
                ('min_kg', models.PositiveIntegerField(default=1)),
                ('max_kg', models.PositiveIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('car', models.ManyToManyField(to='yukuz.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssn', models.IntegerField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PickedOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picked_time', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.Driver')),
                ('picked_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PostOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=3000)),
                ('source_address', models.CharField(max_length=300)),
                ('destination_address', models.CharField(max_length=300)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('order_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.Person', verbose_name='order by a person')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='driver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.Person'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.VehicleType'),
        ),
    ]
