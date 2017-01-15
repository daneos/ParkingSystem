# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_auto_20170114_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freespot',
            name='time_end',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='freespot',
            name='time_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
