# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-18 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0017_documents_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemanager',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
