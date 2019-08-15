# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-12 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('linkout_mgr', '0002_auto_20190702_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneLinkout',
            fields=[
                ('linkoutservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='linkout_mgr.LinkoutService')),
                ('gene_example0', models.CharField(max_length=255)),
            ],
            bases=('linkout_mgr.linkoutservice',),
        ),
        migrations.CreateModel(
            name='GenomicRegionLinkout',
            fields=[
                ('linkoutservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='linkout_mgr.LinkoutService')),
                ('sequence_example', models.CharField(max_length=255)),
                ('start_example', models.CharField(max_length=12)),
                ('end_example', models.CharField(max_length=12)),
            ],
            bases=('linkout_mgr.linkoutservice',),
        ),
        migrations.AlterModelOptions(
            name='linkoutservice',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='linkoutservice',
            old_name='gene_example',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='linkoutservice',
            name='url_prefix',
        ),
        migrations.RemoveField(
            model_name='linkoutservice',
            name='url_suffix',
        ),
        migrations.AddField(
            model_name='linkoutservice',
            name='url_format',
            field=models.CharField(default='', help_text='Uses sprintf format', max_length=255, verbose_name='URL Format'),
            preserve_default=False,
        ),
    ]