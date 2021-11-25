from django.db import models

class Users(models.Model):
    last_name = models.CharField(max_length=255, null=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=255, null=True, verbose_name="Имя")
    middle_name = models.CharField(max_length=255, null=True, verbose_name="Отчество")
    position = models.CharField(max_length=255, null=True, verbose_name="Должность")
    department = models.CharField(max_length=255, null=True, verbose_name="Отдел")
    password = models.CharField(max_length=255, null=True, verbose_name="Пароль")
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "<User: %s %s>" % (self.last_name, self.department,)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class NotifyError(models.Model):
    last_name = models.CharField(max_length=255, null=True, verbose_name="Фамилия")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Error"
        verbose_name_plural = "Errors"