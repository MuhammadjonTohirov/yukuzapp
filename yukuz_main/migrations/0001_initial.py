# Generated by Django 2.1.7 on 2019-03-09 12:53

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
                ('title', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('min_kg', models.PositiveIntegerField(default=1)),
                ('max_kg', models.PositiveIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveringProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Delivering Processes',
            },
        ),
        migrations.CreateModel(
            name='DriverRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='OrderImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='def_user.png', upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='PickedOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picked_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=3000)),
                ('weigth', models.FloatField()),
                ('source_address', models.CharField(max_length=300)),
                ('destination_address', models.CharField(max_length=300)),
                ('is_picked', models.BooleanField(default=False)),
                ('deadline', models.DateField()),
                ('estimated_price', models.FloatField(default=0)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('sign', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
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
            model_name='postorder',
            name='currency_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yukuz_main.PriceClass'),
        ),
    ]
