from django.db import models

from common.utils.string_func import upload_image_path


class TypeChoices(models.TextChoices):
    profile = 'profile', 'profile'


class BaseModel(models.Model):
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارشیو شدن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True


class Media(BaseModel):
    file = models.FileField(upload_to=upload_image_path, verbose_name='فایل')
    file_type = models.CharField(max_length=25, choices=TypeChoices.choices, verbose_name='نوع فایل')

    class Meta:
        verbose_name = "فایل"
        verbose_name_plural = "فایل ها"
