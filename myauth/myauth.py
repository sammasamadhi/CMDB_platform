#_*_coding:utf-8_*_

__author__ = 'alex'

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            #token=token,
            #department=department,
            #tel=tel,
            #memo=memo,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name ,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            name=name,
            #token=token,
            #department=department,
            #tel=tel,
            #memo=memo,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=64,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    name = models.CharField(u'名字', max_length=32)
    token = models.CharField(u'token', max_length=128,default=None,blank=True,null=True)
    department = models.CharField(u'部门', max_length=32,default=None,blank=True,null=True)
    tel = models.CharField(u'座机', max_length=32,default=None,blank=True,null=True)
    mobile = models.CharField(u'手机', max_length=32,default=None,blank=True,null=True)

    memo = models.TextField(u'备注', blank=True,null=True,default=None)
    date_joined = models.DateTimeField(blank=True, auto_now_add=True)
    #valid_begin = models.DateTimeField(blank=True, auto_now=True)

    host_groups = models.ManyToManyField("hosts.HostGroup",blank=True)
    bind_hosts = models.ManyToManyField("hosts.BindHostToUser",blank=True)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"
    def __unicode__(self):
        return self.name

    objects = UserManager()