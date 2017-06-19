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
        managed = True
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
        managed = True
        db_table = 'user'

    def __str__(self):
        return self.name
