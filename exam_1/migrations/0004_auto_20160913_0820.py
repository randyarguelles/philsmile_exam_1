# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_1', '0003_auto_20160913_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='user_answer',
            field=models.ForeignKey(to='exam_1.Choice'),
        ),
    ]
