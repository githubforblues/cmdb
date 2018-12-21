# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-20 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0021_auto_20181220_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=256)),
                ('lastpackagetime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='servicedeployconfig',
            name='projectname',
        ),
        migrations.AddField(
            model_name='servicedeployconfig',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hostmanager.ProjectPackage'),
            preserve_default=False,
        ),
    ]
