from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Helps Django work with the custom User model"""

    def create_user(self, cedula, first_name, last_name, password, type='D', email=None, doctor=None, considerations=None,
                    max_threshold=None, min_threshold=None):
        """Creates and saves a new user profile object"""

        if not cedula:
            raise ValueError('La cedula es obligatoria')

        user = self.model(cedula=cedula, first_name=first_name, last_name=last_name, type=type, email=email,
                          doctor=doctor, considerations=considerations, max_threshold=max_threshold, min_threshold=min_threshold)

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

    USER_TYPE = (
        ('D', 'Doctor'),
        ('P', 'Paciente'),
    )

    cedula = models.CharField(unique=True, max_length=10)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    considerations = models.TextField(null=True, blank=True)
    min_threshold = models.FloatField(null=True, blank=True)
    max_threshold = models.FloatField(null=True, blank=True)
    doctor = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=1, choices=USER_TYPE)
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
        return str(self.cedula)
