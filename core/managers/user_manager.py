from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault(str('is_superuser'), False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault(str('is_superuser'), True)
        extra_fields.setdefault(str('is_staff'), True)
        if extra_fields.get(str('is_superuser')) is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ResetPasswordManager(models.Manager):

    def create_reset_password(self, user):
        key = uuid.uuid1().hex
        reset_password = self.create(user=user, key=key)
        return reset_password
