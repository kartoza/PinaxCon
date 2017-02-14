# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_proposals', '0002_auto_20170214_0051'),
        ('taggit', '0002_auto_20150616_2121'),
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='symposion_proposals.ProposalBase')),
                ('map_image', models.ImageField(help_text=b"Please upload an image of the map. It will be made public on the website. If it's an interactive map, please create a screenshot. The size is limited to 5MB.", upload_to=b'maps', verbose_name=b'Map')),
                ('map_link', models.URLField(help_text=b'This link will be used to link the image on our website to your map. It could be a link to a high resolution version, a webpage with further details or to your interactive map.', verbose_name=b'Link to Map', blank=True)),
                ('foss_using', models.TextField(help_text=b'Please list the Free and open-source software<sup><a href="#fn1" title="Open source definition">1</a></sup> that you\'ve used for creating the map.', verbose_name=b'FOSS software used', blank=True)),
                ('open_data_using', models.TextField(help_text=b'Please list the open data<sup><a href="#fn2" title="Open data definition">2</a></sup> sources that you\'ve used for creating the map.', verbose_name=b'Open data used', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'map proposal',
            },
            bases=('symposion_proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='WorkshopProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='symposion_proposals.ProposalBase')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'workshop proposal',
            },
            bases=('symposion_proposals.proposalbase',),
        ),
        migrations.RemoveField(
            model_name='talkproposal',
            name='audience_level',
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_contributing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_contributing_links',
            field=models.TextField(help_text=b"Please add links some of the contributions you've made", verbose_name=b'Link to contributions', blank=True),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_is',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_is_links',
            field=models.TextField(help_text=b'Please add a link to the source code of your open source project', verbose_name=b'Link to project', blank=True),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_using',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='foss_using_links',
            field=models.TextField(help_text=b'Please add links some of the projects you use', verbose_name=b'Link to projects', blank=True),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
