# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from core.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=20, null=True, blank=True)
