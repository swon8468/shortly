# Generated by Django 5.0.6 on 2024-06-24 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_group_customuser_group_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 24, 12, 2, 8, 700037, tzinfo=datetime.timezone.utc)),
        ),
    ]
