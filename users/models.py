import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, age, password=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user  = self.model(email=email, name=name, age=age)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name    = models.CharField(max_length=100)
    email   = models.EmailField(unique=True)
    age     = models.IntegerField()
    password = models.CharField(max_length=255)
    avatar  = models.ImageField(upload_to='avatars/', null=True, blank=True)  # ← new

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name', 'age']

    def __str__(self):
        return self.email