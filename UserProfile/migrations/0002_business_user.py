# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-02 16:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]