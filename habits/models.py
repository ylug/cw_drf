from django.db import models

from django.contrib.auth import get_user_model
from users.models import NULLABLE

class Habit(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user', verbose_name='пользователь')
    place = models.CharField(max_length=150, verbose_name="место")
    time = models.TimeField(verbose_name='время когда выполнять')
    action = models.CharField(max_length=150, verbose_name="действие")
    sign_of_pleasant = models.BooleanField(default=False, verbose_name="признак приятной привычки")
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, verbose_name="связанная привычка", **NULLABLE)
    periodicity = models.SmallIntegerField(default=1, verbose_name="периодичность")
    reward = models.CharField(max_length=150, verbose_name="вознаграждение", **NULLABLE)
    time_to_complete = models.DurationField(verbose_name="время на выполнение", **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    next_date = models.DateField(**NULLABLE, verbose_name="дата следующего действия")

    def __str__(self):
        return f'{self.user} будет {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('id',)
