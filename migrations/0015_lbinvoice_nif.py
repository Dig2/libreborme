# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-26 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0014_auto_20170226_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='lbinvoice',
            name='nif',
            field=models.CharField(default='764223232F', max_length=20),
            preserve_default=False,
        ),
    ]
