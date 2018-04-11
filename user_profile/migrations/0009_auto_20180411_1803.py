# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-11 10:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_auto_20180411_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verification_code',
            field=models.CharField(default=b'1530', max_length=4, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]
