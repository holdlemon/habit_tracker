from rest_framework import serializers

from habits.models import Habits
from habits.validators import validate_execution_time, validate_periodicity, validate_award_and_related_habit, \
    validate_pleasant_habit, validate_related_habit_is_pleasant


class HabitsSerializer(serializers.ModelSerializer):

    # Подключаем валидатор
    def validate(self, data):
        # Создаём временный объект Habit для передачи в валидаторы
        habit = Habits(**data)

        # Вызываем валидаторы
        validate_award_and_related_habit(habit)
        validate_execution_time(habit)
        validate_related_habit_is_pleasant(habit)
        validate_pleasant_habit(habit)
        validate_periodicity(habit)

        # Возвращаем данные, если все валидации прошли успешно
        return data

    class Meta:
        model = Habits
        fields = "__all__"