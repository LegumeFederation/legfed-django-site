# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-27 23:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_mgr', '0012_auto_20181105_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resource_mgr.Resource')),
            ],
            options={
                'ordering': ['analysis_type', 'text'],
            },
            bases=('resource_mgr.resource',),
        ),
        migrations.CreateModel(
            name='ToolAnalysisType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ToolDataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='tool',
            name='analysis_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resource_mgr.ToolAnalysisType'),
        ),
        migrations.AddField(
            model_name='tool',
            name='input_data_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tool_input_data_type', to='resource_mgr.ToolDataType'),
        ),
        migrations.AddField(
            model_name='tool',
            name='output_data_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tool_output_data_type', to='resource_mgr.ToolDataType'),
        ),
    ]
