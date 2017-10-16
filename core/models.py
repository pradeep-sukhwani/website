# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from core.managers.user_manager import UserManager, ResetPasswordManager


class User(AbstractBaseUser, PermissionsMixin):
    MALE = 1
    FEMALE = 2
    PREFERRED_NOT_TO_SAY = 3
    GENDER_PREFERENCES = ((MALE, 'MALE'), (FEMALE, 'FEMALE'), (PREFERRED_NOT_TO_SAY, 'PREFERRED_NOT_TO_SAY'))

    email = models.EmailField(_('email address'), unique=True, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True)
    gender = models.SmallIntegerField(choices=GENDER_PREFERENCES, default=MALE)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def is_admin(self):
        if self.groups.filter(name="admin"):
            return True
        return False

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ResetPassword(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    objects = ResetPasswordManager()
