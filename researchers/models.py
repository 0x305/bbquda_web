from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# BRIAN NOTE:  Was unable to refactor function names for MyAccountManager.
# Otherwise, it would cause problems when creating new researcher accounts or super users.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, username= None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            
           
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Researcher(AbstractUser):
    email = models.EmailField(verbose_name = "email", max_length=254, unique = True)
    first_name = models.CharField(max_length =30,blank=True, null=True)
    last_name = models.CharField(max_length = 30,blank=True, null=True)
    username = models.CharField( max_length=30, unique = True)
    
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

