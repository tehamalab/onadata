# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0023_auto_20160419_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='xform',
            name='has_hxl_support',
            field=models.BooleanField(default=False),
        ),
    ]