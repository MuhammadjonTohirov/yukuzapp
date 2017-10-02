# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 20:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz', '0003_auto_20170924_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='yukuz', to=settings.AUTH_USER_MODEL),
        ),
    ]
