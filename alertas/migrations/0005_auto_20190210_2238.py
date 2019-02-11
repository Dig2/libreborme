# Generated by Django 2.0.10 on 2019-02-10 21:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0002_auto_20180627_1121'),
        ('alertas', '0004_auto_20190210_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertaacto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertaacto',
            name='stripe_subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='djstripe.Subscription'),
            preserve_default=False,
        ),
    ]
