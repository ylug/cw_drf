from rest_framework import serializers

from habits.models import Habit
from habits.validators import completion_duration, choose_related_habit_or_reward, long_execution_time, \
    pleasant_format, related_is_pleasant

class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для привычки
    """
    class Meta:
        model = Habit
        fields = '__all__'
        """
        Дополнительная валидация для сериализатора
        """
        validators = [
        choose_related_habit_or_reward,
        long_execution_time,
        related_is_pleasant,
        pleasant_format,
        completion_duration,
        ]
