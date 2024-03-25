from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser, Group, Permission, PermissionsMixin
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField('email', max_length=255, unique=True, )
    # name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    # last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    # image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} {self.username}'


# class User(AbstractUser):
#     email = models.EmailField('emial', unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username
#
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name='calendar_app_user_set'  # Cambia el nombre del related_name
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         related_name='calendar_app_user_set'  # Cambia el nombre del related_name
#     )


# Create your models here.
class Event(models.Model):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def user_info(self):
        return {
            'id': self.user.id,
            'username': self.user
        }

    # objects = EventManager()

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
