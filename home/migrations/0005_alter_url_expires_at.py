# Generated by Django 5.0.6 on 2024-06-24 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_url_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 24, 12, 4, 46, 842445, tzinfo=datetime.timezone.utc)),
        ),
    ]
