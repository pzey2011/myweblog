# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-11 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20171111_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='/home/peyman/django_projects/myweblog/media/user-default.jpg', null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
    ]
