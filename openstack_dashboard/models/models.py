# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    os_id = models.CharField(max_length=40)
    start = models.DateTimeField()
    state = models.IntegerField(blank=True, null=True)
    remaining = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'project'

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255, blank=True, null=True)
    idp = models.CharField(max_length=30)
    cn = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    duration = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, db_column='project', blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return self.name
