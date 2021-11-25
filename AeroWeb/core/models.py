from datetime import datetime as dt

from django.db import models

class Users(models.Model):
    last_name = models.CharField(max_length=255, null=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=255, null=True, verbose_name="Имя")
    middle_name = models.CharField(max_length=255, null=True, verbose_name="Отчество")
    position = models.CharField(max_length=255, null=True, verbose_name="Должность")
    department = models.CharField(max_length=255, null=True, verbose_name="Отдел")
    password = models.CharField(max_length=255, null=True, verbose_name="Пароль")
    created = models.DateTimeField(editable=True, default=dt.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.middle_name,)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class NotifyError(models.Model):
    last_name = models.CharField(max_length=255, null=True, verbose_name="Фамилия")
    text = models.TextField()
    created = models.DateTimeField(editable=True)

    def __str__(self):
        return "%s" % (self.last_name,)

    class Meta:
        verbose_name = "Error"
        verbose_name_plural = "Errors"