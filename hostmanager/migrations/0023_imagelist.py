# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-21 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0022_auto_20181220_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagename', models.CharField(max_length=256)),
            ],
        ),
    ]