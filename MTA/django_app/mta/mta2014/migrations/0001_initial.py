# Generated by Django 2.1.7 on 2019-03-26 06:27

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NYCBoroughs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borocode', models.IntegerField()),
                ('boroname', models.CharField(max_length=32)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='RouteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.CharField(max_length=4)),
                ('agency_id', models.CharField(max_length=32)),
                ('route_short_name', models.CharField(max_length=4)),
                ('route_long_name', models.CharField(max_length=64)),
                ('route_desc', models.CharField(max_length=4096)),
                ('route_type', models.IntegerField()),
                ('route_url', models.CharField(max_length=128)),
                ('route_color', models.CharField(max_length=16, null=True)),
                ('route_text_color', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shapes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape_id', models.CharField(max_length=50)),
                ('route_name', models.CharField(max_length=4)),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('routeinfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mta2014.RouteInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_id', models.CharField(max_length=50)),
                ('stop_code', models.CharField(max_length=50)),
                ('stop_name', models.CharField(max_length=50)),
                ('stop_desc', models.CharField(max_length=50)),
                ('zone_id', models.CharField(max_length=50)),
                ('stop_url', models.CharField(max_length=50)),
                ('location_type', models.IntegerField()),
                ('parent_station', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Timestamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updateid', models.IntegerField()),
                ('stop_number', models.IntegerField()),
                ('arrival', models.FloatField(null=True)),
                ('departure', models.FloatField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_stop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_stop_trips', to='mta2014.Stops')),
                ('header_timestamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mta2014.Timestamp')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mta2014.RouteInfo')),
                ('start_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mta2014.Date')),
                ('stop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stop_trips', to='mta2014.Stops')),
            ],
        ),
        migrations.CreateModel(
            name='TripName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mta2014.TripName'),
        ),
    ]
