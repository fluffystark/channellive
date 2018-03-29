# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-27 02:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive', models.CharField(blank=True, default='', max_length=200)),
                ('video', models.URLField(blank=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Livestream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_live', models.BooleanField(default=False)),
                ('session', models.CharField(max_length=200)),
                ('archive', models.CharField(blank=True, default='', max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='livestream_pic')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livestreams', to='event.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livestreams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField(default=False)),
                ('livestream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewers', to='OpenTokHandler.Livestream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='archive',
            name='livestream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archives', to='OpenTokHandler.Livestream'),
        ),
    ]
