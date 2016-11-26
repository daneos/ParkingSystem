# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('plate', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('data', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FreeSpot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('session_hash', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('amount', models.FloatField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionMethod',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('balance', models.FloatField()),
                ('owner_id', models.ForeignKey(to='rest.User')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='method_id',
            field=models.ForeignKey(to='rest.TransactionMethod'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_id',
            field=models.ForeignKey(to='rest.Wallet'),
        ),
        migrations.AddField(
            model_name='spot',
            name='owner_id',
            field=models.ForeignKey(related_name='+', to='rest.User'),
        ),
        migrations.AddField(
            model_name='spot',
            name='parking_id',
            field=models.ForeignKey(to='rest.Parking'),
        ),
        migrations.AddField(
            model_name='spot',
            name='user_id',
            field=models.ForeignKey(related_name='+', to='rest.User'),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='spot_id',
            field=models.ForeignKey(to='rest.Spot'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_id',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='freespot',
            name='spot_id',
            field=models.ForeignKey(to='rest.Spot'),
        ),
        migrations.AddField(
            model_name='code',
            name='parking_id',
            field=models.ForeignKey(to='rest.Parking'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner_id',
            field=models.ForeignKey(to='rest.User'),
        ),
    ]
