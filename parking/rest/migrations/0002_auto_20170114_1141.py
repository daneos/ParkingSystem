# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='owner_id',
            field=models.ForeignKey(related_name='+', blank=True, to='rest.User', null=True),
        ),
        migrations.AlterField(
            model_name='spot',
            name='user_id',
            field=models.ForeignKey(related_name='+', blank=True, to='rest.User', null=True),
        ),
    ]
