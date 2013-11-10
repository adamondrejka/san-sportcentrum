# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        """ Makes new user and sets his password. Creates random one if password is not set.

        :param email: user email
        :param password: user password
        :param is_active: if user is active after creating or not
        :return: user and user password (for email information) :raise ValueError:
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=UserManager.normalize_email(email))
        user_password = password
        user.set_password(user_password)
        user.is_active = is_active
        user.save(using=self._db)
        return user, user_password

    def create_superuser(self, email, password=None):
        user, password = self.create_user(email, password)

        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
