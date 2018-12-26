# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-24 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0025_servicedeploylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicedeploylist',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostmanager.ServiceDeployStatus'),
        ),
        migrations.AlterField(
            model_name='servicedeploystatus',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostmanager.ServiceDeployConfig'),
        ),
    ]