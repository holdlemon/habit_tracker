from django.db import models

from config.settings import AUTH_USER_MODEL


class Habits(models.Model):
    '''Модель привычки'''

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность в днях')
    award = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    execution_time = models.PositiveIntegerField(default=60, verbose_name="Время выполнения в секундах")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f'{self.user} - {self.action} - {self.time} - {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ["pk"]
