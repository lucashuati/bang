# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='secret_key_coach',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='group',
            name='secret_key_visitor',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
