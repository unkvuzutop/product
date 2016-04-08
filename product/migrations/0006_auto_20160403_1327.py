# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20160402_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='^[a-zA-Z0-9\u0430-\u044f-\u0410-\u042f]*$', message=b'Username must be Alphanumeric', code=b'invalid_username')]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(20)]),
        ),
    ]
