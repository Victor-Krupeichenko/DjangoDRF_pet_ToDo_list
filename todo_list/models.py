from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Table Task"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=250, verbose_name="Описание задачи")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    execute_status = models.BooleanField(default=False, verbose_name="Статус выполнения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["date_create", "title"]
