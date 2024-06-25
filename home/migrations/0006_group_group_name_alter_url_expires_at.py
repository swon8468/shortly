# Generated by Django 5.0.6 on 2024-06-25 03:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_url_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 25, 3, 45, 51, 515976, tzinfo=datetime.timezone.utc)),
        ),
    ]