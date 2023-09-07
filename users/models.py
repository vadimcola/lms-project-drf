from django.contrib.auth.models import AbstractUser
from django.db import models

from users.manager import CustomUserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True)
    city = models.CharField(max_length=35, verbose_name='Город', blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь сервиса'
        verbose_name_plural = 'Пользователи сервиса'
