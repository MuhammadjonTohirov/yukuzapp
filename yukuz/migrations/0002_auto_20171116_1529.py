# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yukuz_auth', '0001_initial'),
        ('yukuz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postorder',
            name='order_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_auth.Person', verbose_name='order by a person'),
        ),
        migrations.AddField(
            model_name='postorder',
            name='type_of_vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz.VehicleType'),
        ),
        migrations.AddField(
            model_name='pickedorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.PostOrder'),
        ),
        migrations.AddField(
            model_name='pickedorder',
            name='picked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_auth.Driver'),
        ),
        migrations.AddField(
            model_name='orderimages',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_image', to='yukuz.PostOrder'),
        ),
        migrations.AddField(
            model_name='driverrate',
            name='star_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_auth.Person'),
        ),
        migrations.AddField(
            model_name='driverrate',
            name='star_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz.PickedOrder'),
        ),
        migrations.AddField(
            model_name='car',
            name='by_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_auth.Person'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yukuz.VehicleType'),
        ),
    ]
