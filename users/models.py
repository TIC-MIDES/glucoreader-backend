from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Helps Django work with the custom User model"""

    def create_user(self, cedula, first_name, last_name, password=None):
        """Creates and saves a new user profile object"""

        if not cedula:
            raise ValueError('El email es obligatorio')

        user = self.model(cedula=cedula, first_name=first_name, last_name=last_name)

        user.set_password(password)  # esto hashea las passwords
        user.save(using=self._db)

        return user

    def create_superuser(self, cedula, first_name, last_name, password):
        """Creates and saves a new user profile object"""

        user = self.create_user(cedula, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    cedula = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    doctor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    """ Los siguiente campos son necesarios porque los pide Django, por ahora nosotros no los usamos """
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
