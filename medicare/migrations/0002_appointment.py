# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-24 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicare.Doctorprofile')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicare.Studentprofile')),
            ],
        ),
    ]
