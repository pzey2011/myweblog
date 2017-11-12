# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-11 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20171111_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='/account/user-default.jpg', null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
    ]