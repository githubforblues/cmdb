# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-22 04:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0008_auto_20181022_0406'),
    ]

    operations = [
        migrations.CreateModel(
            name='EteamsHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostinstancename', models.CharField(max_length=100)),
                ('hostname', models.CharField(max_length=100, unique=True)),
                ('hostipaddr', models.CharField(max_length=100)),
                ('hosttype', models.IntegerField()),
                ('hostdesc', models.CharField(max_length=500)),
                ('hoststatus', models.IntegerField()),
            ],
        ),
    ]
