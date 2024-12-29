from django.db import models

from core.models import BaseModel


class StatusChoices(models.TextChoices):
    accept = 'ac', 'accept'
    reject = 're', 'reject'


class LoginLog(BaseModel):
    updated_at = None
    car = models.ForeignKey('resources.Cars', on_delete=models.CASCADE, verbose_name='ماشین')
    status = models.CharField(choices=StatusChoices.choices, verbose_name='نتیجه ورود', max_length=5)

    class Meta:
        verbose_name = 'گزارش ورود'
        verbose_name_plural = 'گزارش های ورود'


class LogoutLog(BaseModel):
    updated_at = None
    car = models.ForeignKey('resources.Cars', on_delete=models.CASCADE, verbose_name='ماشین')

    class Meta:
        verbose_name = 'گزارش خروج'
        verbose_name_plural = 'گزارش های خروج'
