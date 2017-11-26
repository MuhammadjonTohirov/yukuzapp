# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 04:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz', '0004_remove_car_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz.VehicleType'),
        ),
    ]
