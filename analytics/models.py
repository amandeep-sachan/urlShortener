# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from shortener.models import DjangoURL

class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, DjangoURL):
            obj, create = self.get_or_create(django_url = instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    django_url = models.OneToOneField(DjangoURL)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)