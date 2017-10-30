# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 05:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz', '0003_auto_20171029_0422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useravatar',
            name='owner',
        ),
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(default='def_user', upload_to='', verbose_name='image/def_user'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='driver', serialize=False, to='yukuz.Person'),
        ),
        migrations.DeleteModel(
            name='UserAvatar',
        ),
    ]
