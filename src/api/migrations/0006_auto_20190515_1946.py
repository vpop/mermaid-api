# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-15 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190515_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='benthictransect',
            name='collect_record_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fishbelttransect',
            name='collect_record_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quadratcollection',
            name='collect_record_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
