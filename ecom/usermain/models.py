from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, password, **extra_fields)
class Users(AbstractUser):
    username = None
    last_login = None
    first_name = models.CharField(("firts_name"), max_length=20,null=False)
    last_name = models.CharField(("second_name"), max_length=50)
    email = models.EmailField(("email"), max_length=254,unique=True)
    Number = models.BigIntegerField(unique=True)
    Address = models.TextField(("Address"),null=False)
    Gender = models.CharField(("Gender"), max_length=20,null=True)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['first_name','Number',]
    
    objects = UserManager()
    def __str__(self) :
        return self.first_name 