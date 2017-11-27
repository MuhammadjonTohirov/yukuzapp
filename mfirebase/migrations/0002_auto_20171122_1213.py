# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mfirebase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobdevice',
            name='id',
        ),
        migrations.AlterField(
            model_name='mobdevice',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mfirebase.DeviceType'),
        ),
        migrations.AlterField(
            model_name='mobdevice',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='yukuz_auth.Person'),
        ),
    ]