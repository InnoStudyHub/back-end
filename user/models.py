from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


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
    study_year = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    favourite_decks = models.ManyToManyField('deck.Deck')
    iu_refresh_token = models.CharField(max_length=4096, default='', null=True)
    iu_access_token = models.CharField(max_length=4096, default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserAnalytic(models.Model):
    id = models.AutoField(primary_key=True)
    user_analytic_id = models.IntegerField()
    studyhub_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_analytic'

