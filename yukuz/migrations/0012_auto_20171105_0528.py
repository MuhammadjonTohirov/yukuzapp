# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz', '0011_auto_20171101_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postorder',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
