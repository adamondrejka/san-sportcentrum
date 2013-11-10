# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        without_password = kwargs.get('without_password')

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password) and not without_password:
                return user
            elif without_password:
                return user
        except UserModel.DoesNotExist:
            return None
