from django.db import models

# standard base class for overriding the default Django User model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
  """Manager for user profiles"""


  def create_user(self, email, name, password=None):
    """Create a new user profile"""
    if not email:
      raise ValueError('User must have an email address')

    email = self.normalize_email(email)
    user = self.model(email=email, name=name)

    user.set_password(password)#encrypts the password
    user.save(using=self.__db__) #Django supports multiple dbs

    return user

  def create_super_user(self, email, name, password):
    """Create and save a new superuser with given details"""
    user = self.create_user(email, name, password)

    user.is_superuser = True # automatically created by the PermissionsMixin
    user.is_staff = True
    user.save(using=self.__db__)

    return user


# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
  """Database model for users in the system"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserProfileManager()

  # overwrites the default username field with the user's email field
  USERNAME_FIELD = 'email' # required by default
  REQUIRED_FIELD = ['name']

  def get_full_name(self):
    """Retrieves full name of user"""
    return self.name

  def get_short_name(self):
    """Retrives short name of user"""
    return self.name

  def __str__(self):
    """Returns string representation of our user"""
    return self.email


