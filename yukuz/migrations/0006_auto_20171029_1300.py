# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz', '0005_auto_20171029_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceclass',
            name='sign',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='priceclass',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]