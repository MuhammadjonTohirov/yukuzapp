# Generated by Django 2.1.7 on 2019-03-07 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yukuz_oauth', '0007_remove_uuser_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MobDevice',
            fields=[
                ('added', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('device', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=50)),
                ('is_driver', models.BooleanField(default=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_firebase.DeviceType')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_oauth.Person')),
            ],
        ),
    ]