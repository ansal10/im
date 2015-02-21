# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('is_sealed', models.BooleanField(default=False, verbose_name='Sealed')),
                ('status', models.CharField(db_index=True, max_length=255, verbose_name='Status', choices=[(b'ACTIVE', 'Active'), (b'WINS', 'Winner'), (b'DEL', 'Deleted'), (b'PAID', 'Paid'), (b'UNPAID', 'Unpaid'), (b'CLOSE', 'Closed')])),
                ('amount', models.FloatField(default=0, max_length=255, verbose_name='Amount', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('deliever_by', models.DateTimeField(verbose_name='Deliever By')),
                ('deleted_on', models.DateTimeField(default=None, null=True, verbose_name='Deleted On', db_index=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=None, auto_now=True, null=True, verbose_name='Last Updated On')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Filename')),
                ('extension', models.CharField(max_length=255, verbose_name='extension')),
                ('deleted_on', models.DateTimeField(default=None, null=True, verbose_name='Deleted On', db_index=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('content', models.FileField(upload_to=models.CharField(max_length=255, verbose_name='Filename'))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('status', models.CharField(db_index=True, max_length=255, choices=[(b'READ', 'Read'), (b'UNREAD', 'Not Read')])),
                ('reciever', models.ForeignKey(related_name='reciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile', models.CharField(max_length=255, choices=[(b'SCHOLAR', 'Scholar'), (b'STUD', 'Student')])),
                ('balance', models.FloatField(default=0, max_length=255, verbose_name='Balance', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('category', models.CharField(max_length=255, choices=[(b'NEW', 'New Student'), (b'OLD', 'Old Student'), (b'FRESHER', 'Fresher'), (b'EXPERIENCE', 'Experienced'), (b'EXPERT', 'Expert')])),
                ('degree', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned_on', models.DateTimeField(null=True, verbose_name='Alloted on')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('amount', models.FloatField(default=0, max_length=255, verbose_name='Budget', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('deleted_on', models.DateTimeField(default=None, null=True, verbose_name='Deleted On', db_index=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=None, auto_now=True, null=True, verbose_name='Last Updated On')),
                ('due_on', models.DateTimeField(verbose_name='Due on')),
                ('status', models.CharField(db_index=True, max_length=255, choices=[(b'LIVE', 'Live'), (b'PROG', 'In Progress'), (b'COMP', 'Completed'), (b'DISP', 'Disputed'), (b'EXPR', 'Expired')])),
                ('assigned_to', models.ForeignKey(related_name='assigned', verbose_name='Alloted to', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('deleted_on', models.DateTimeField(default=None, null=True, verbose_name='Deleted On', db_index=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=None, auto_now=True, null=True, verbose_name='Last Updated On')),
                ('project', models.ForeignKey(to='hw.Project')),
                ('upload1', models.ForeignKey(related_name='solution_upload1', verbose_name='File 1', blank=True, to='hw.File', null=True)),
                ('upload2', models.ForeignKey(related_name='solution_upload2', verbose_name='File 2', blank=True, to='hw.File', null=True)),
                ('upload3', models.ForeignKey(related_name='solution_upload3', verbose_name='File 3', blank=True, to='hw.File', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('deleted_on', models.DateTimeField(default=None, null=True, verbose_name='Deleted On', db_index=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='subject',
            field=models.ForeignKey(to='hw.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='upload1',
            field=models.ForeignKey(related_name='project_upload1', verbose_name='File 1', blank=True, to='hw.File', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='upload2',
            field=models.ForeignKey(related_name='project_upload2', verbose_name='File 2', blank=True, to='hw.File', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='upload3',
            field=models.ForeignKey(related_name='project_upload3', verbose_name='File 3', blank=True, to='hw.File', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='project',
            field=models.ForeignKey(to='hw.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
