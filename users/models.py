from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils.safestring import mark_safe
from datetime import datetime


# Create your models here.

class UserManager(BaseUserManager):
    """ custom manager is use to tell django to use email instead of username"""
    

    def create_user(self, first_name, last_name, email, provider, password=None, **extra_fields):
        """ create a user """
        if not email:
            raise ValueError("Email is required. *****")

        email_lower = email
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email_lower.lower()),
            provider = provider,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name,  email, provider, password=None, **extra_fields):
        """ define how a superuser is created """
        email_lowercase = email
        user = self.create_user(first_name, last_name, email_lowercase.lower(), provider,  password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
#

class User(AbstractBaseUser, PermissionsMixin):
    """ Create custom user model/ table details for login """

    email = models.EmailField(verbose_name = 'email address', max_length = 255, unique = True)
    first_name = models.CharField(verbose_name = 'first name', max_length = 255)
    last_name = models.CharField(verbose_name = 'last name', max_length = 255)
    phone_no = models.CharField(max_length = 13, default=0)
    provider = models.CharField(verbose_name='provider', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)
    # last_login = models.DateTimeField(datetime.now, default='2000-01-01')
    login = models.DateTimeField(datetime.now, default='2000-01-01')
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'provider']


    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name():
        return self.first_name
        


class ConfirmEmail(models.Model):
    user = models.EmailField(verbose_name = 'email address', max_length = 255)
    code = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return 'Code' + ' ({})'.format(self.user)