# Generated by Django 2.1.7 on 2019-03-04 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yukuz_oauth', '0004_remove_person_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uuser',
            options={'verbose_name': 'User'},
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(default='image/def_user', upload_to='images/users', verbose_name='image'),
        ),
    ]
