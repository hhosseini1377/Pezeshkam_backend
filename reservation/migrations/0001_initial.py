# Generated by Django 3.0.8 on 2020-08-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=2)),
                ('month', models.CharField(max_length=2)),
                ('year', models.CharField(max_length=4)),
                ('start_hour', models.CharField(max_length=2)),
                ('start_minute', models.CharField(max_length=2)),
                ('end_hour', models.CharField(max_length=2)),
                ('end_minute', models.CharField(max_length=2)),
            ],
        ),
    ]
