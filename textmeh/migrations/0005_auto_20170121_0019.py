# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textmeh', '0004_auto_20170120_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlanguage',
            name='language_code',
            field=models.CharField(default='testy', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userlanguage',
            name='language',
            field=models.CharField(max_length=50),
        ),
    ]
