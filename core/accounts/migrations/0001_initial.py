# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-09 21:52
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], help_text="Choices: ['male', 'female']", max_length=10, null=True, verbose_name='Gender')),
                ('avatar', models.ImageField(blank=True, default='/media/user-default.jpg', null=True, upload_to='avatars', verbose_name='Avatar')),
            ],
            options={
                'verbose_name_plural': 'Profiles',
                'verbose_name': 'Profile',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
