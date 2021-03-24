from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email,  password, username=None, organization=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
           
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#All logged in users would be researchers
class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name = "email", max_length=254, unique = True)
    first_name = models.CharField(max_length =30,blank=True, null=True)
    last_name = models.CharField(max_length = 30,blank=True, null=True)
    username = models.CharField( max_length=30, blank=True, null=True)
    organization = models.CharField( max_length=50, blank=True, null=True)
    #let's make this dropdown option in future commits
    research_area = models.CharField( max_length=30, blank=True, null=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'organization']

    def __str__(self):
        if self.first_name:
            return self.first_name+" "+self.last_name
        elif self.last_name:
            return "unamed_first "+self.last_name
        else:
            return "Nonetyped naming"

