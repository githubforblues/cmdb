# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-23 07:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0010_auto_20181022_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='JumpServerAccountManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ServerAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=64)),
                ('password', models.CharField(default='123456', max_length=64)),
                ('hostid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostmanager.EteamsHost')),
            ],
        ),
        migrations.AddField(
            model_name='jumpserveraccountmanager',
            name='serveraccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostmanager.ServerAccount'),
        ),
        migrations.AddField(
            model_name='jumpserveraccountmanager',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostmanager.SystemUser'),
        ),
    ]
