# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-12 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OpenTokHandler', '0007_remove_viewer_is_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='video',
            field=models.URLField(blank=True, default='', max_length=400),
        ),
    ]
