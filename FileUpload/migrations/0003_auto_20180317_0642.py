# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-17 06:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FileUpload', '0002_auto_20180317_0529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventimage',
            old_name='image',
            new_name='file',
        ),
    ]
