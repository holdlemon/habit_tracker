from rest_framework.exceptions import ValidationError


def validate_award_and_related_habit(habit):
    """Проверка, что не указаны одновременно вознаграждение и связанная привычка."""
    if habit.award and habit.related_habit:
        raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")


def validate_execution_time(habit):
    """Проверка, что время выполнения не превышает 120 секунд."""
    if habit.execution_time > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_related_habit_is_pleasant(habit):
    """Проверка, что связанная привычка является приятной."""
    if habit.related_habit and not habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")


def validate_pleasant_habit(habit):
    """Проверка, что у приятной привычки нет вознаграждения или связанной привычки."""
    if habit.is_pleasant and (habit.award or habit.related_habit):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


def validate_periodicity(habit):
    """Проверка, что привычка выполняется не реже, чем 1 раз в 7 дней."""
    if habit.periodicity > 7:
        raise ValidationError("Привычку нельзя выполнять реже, чем 1 раз в 7 дней.")
    if habit.periodicity == 0:
        raise ValidationError("Привычка должна выполняться хотя бы раз в 7 дней.")
