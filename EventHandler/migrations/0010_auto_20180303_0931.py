# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-03 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventHandler', '0009_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, default='Cebu', max_length=50, null=True),
        ),
    ]