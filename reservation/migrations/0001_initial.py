# Generated by Django 3.0.8 on 2020-08-01 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
