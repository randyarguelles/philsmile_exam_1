# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_1', '0002_auto_20160909_0547'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='user_answer',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='user_score',
        ),
        migrations.AddField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='session',
            field=models.ForeignKey(to='exam_1.UserSession'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='user_answer',
            field=models.ForeignKey(default=b'', to='exam_1.Choice'),
        ),
    ]
