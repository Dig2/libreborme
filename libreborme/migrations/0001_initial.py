# Generated by Django 2.0.3 on 2018-05-31 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('free', 'Gratuita'), ('paid', 'Premium'), ('test', 'Período de prueba')], max_length=4)),
                ('notification_method', models.CharField(choices=[('email', 'E-mail'), ('url', 'URL')], default='email', max_length=10)),
                ('notification_email', models.EmailField(blank=True, max_length=254)),
                ('notification_url', models.URLField(blank=True)),
                ('language', models.CharField(choices=[('es', 'Español')], default='es', max_length=3)),
                ('send_html', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
