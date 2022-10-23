from datetime import datetime, timedelta

import jwt
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from studyhub import settings


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not fullname:
            raise ValueError('Users must have a full name')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        user = self.create_user(
            email=email,
            fullname=fullname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    fullname = models.CharField(verbose_name='Fullname', max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    favourite_decks = models.ManyToManyField('deck.Deck')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [fullname]

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
