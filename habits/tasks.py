from celery import shared_task
from .services import send_message


@shared_task
def send_habit_creation_notification(chat_id, habit_details):
    """
    Отправляет уведомление в Telegram о создании привычки.
    :param chat_id: ID чата пользователя.
    :param habit_details: Детали привычки (например, место, время, действие).
    """
    message = (
        f"Новая привычка создана:\n"
        f"Место: {habit_details['place']}\n"
        f"Действие: {habit_details['action']}\n"
        f"Время: {habit_details['time']}"
    )
    send_message(message, chat_id)