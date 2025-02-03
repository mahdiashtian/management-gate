from django.db import models

from core.models import BaseModel


class ModelChoices(models.TextChoices):
    peugeot_207 = 'peugeot_207', 'peugeot 207'
    peugeot_405 = 'peugeot_405', 'peugeot 405'


class ColorChoices(models.TextChoices):
    blue = 'blue', 'blue'


class StatusChoices(models.TextChoices):
    accept = 'accept', 'accept'
    pending = 'pending', 'pending'
    reject = 'reject', 'reject'


class TypeChoices(models.TextChoices):
    citizen = 'citizen', 'citizen'


class LicensePlate(models.Model):
    section_1 = models.CharField(max_length=12, null=True, blank=True, verbose_name='بخش اول')
    section_2 = models.CharField(max_length=12, null=True, blank=True, verbose_name='بخش دوم')
    section_3 = models.CharField(max_length=12, null=True, blank=True, verbose_name='بخش سوم')
    section_4 = models.CharField(max_length=12, null=True, blank=True, verbose_name='بخش چهارم')
    type = models.CharField(max_length=10, choices=TypeChoices, verbose_name='مدل')


class Cars(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='مالک')
    license_plate = models.OneToOneField(LicensePlate, on_delete=models.CASCADE)
    model = models.CharField(choices=ModelChoices.choices, default=ModelChoices.peugeot_405, verbose_name='مدل',
                             max_length=20)
    color = models.CharField(choices=ColorChoices.choices, default=ColorChoices.blue, verbose_name='رنگ', max_length=10)

    class Meta:
        verbose_name = "ماشین"
        verbose_name_plural = "ماشین ها"


class EntryPermits(BaseModel):
    car = models.OneToOneField(Cars, verbose_name='ماشین', on_delete=models.CASCADE)
    entry_count = models.PositiveIntegerField(default=10, verbose_name='تعداد دفعات مجاز')
    expiration = models.DateTimeField(verbose_name='تاریخ انقضا')
    notes = models.TextField(blank=True, verbose_name='توضیحات')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, verbose_name='وضعیت',
                              default=StatusChoices.pending)

    class Meta:
        verbose_name = "مجوز"
        verbose_name_plural = "مجوز ها"
