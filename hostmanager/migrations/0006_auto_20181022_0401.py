# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-22 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0005_auto_20181022_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='username',
            field=models.CharField(default='admin', max_length=64),
        ),
    ]
