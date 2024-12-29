from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    profile = models.OneToOneField('core.Media', on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="نمایه کاربر")
    phone_number = models.CharField(max_length=13,
                                    validators=[
                                        RegexValidator(
                                            regex='^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$',
                                            message='شماره تلفن صحیح نیست',
                                            code='invalid_phone_number')
                                    ],
                                    verbose_name="شماره تلفن"
                                    , null=True, blank=True)
    role = models.CharField(
        max_length=50,
        choices=[('admin', 'Admin'), ('user', 'User'), ('guest', 'Guest')],
        default='user',
        verbose_name='نقش کاربر'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        app_label = 'users'
