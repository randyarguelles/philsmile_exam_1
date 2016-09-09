# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exam_1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='answered_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='user_answer',
            field=models.ForeignKey(default=b'', to='exam_1.Choice'),
        ),
    ]
