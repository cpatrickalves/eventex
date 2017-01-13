# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-13 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import eventex.subscriptions.validators


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20161117_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='cpf',
            field=models.CharField(max_length=11, validators=[eventex.subscriptions.validators.validate_cpf], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Telefone'),
        ),
    ]
