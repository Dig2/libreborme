# Generated by Django 2.0.3 on 2018-09-01 15:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borme', '0007_company_date_dissolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='auditors',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
