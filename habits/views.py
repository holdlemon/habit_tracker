from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner

from .models import Habits
from .paginators import FiveItemsPaginator
from .serializers import HabitsSerializer
from .tasks import send_habit_creation_notification


class HabitsCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        # Сохраняем привычку
        habit = serializer.save(user=self.request.user)

        # Если у пользователя есть tg_chat_id, отправляем уведомление
        if self.request.user.tg_chat_id:
            habit_details = {
                "place": habit.place,
                "action": habit.action,
                "time": habit.time.strftime("%H:%M:%S"),  # Преобразуем время в строку
            }
            send_habit_creation_notification.delay(
                chat_id=self.request.user.tg_chat_id,
                habit_details=habit_details
            )


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """Получение одной привычки"""

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsListAPIView(generics.ListAPIView):
    """Получение списка привычек"""

    serializer_class = HabitsSerializer
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        user = self.request.user
        return Habits.objects.filter(user=user)


class HabitsPublicListAPIView(generics.ListAPIView):
    """Получение списка публичных привычек"""

    serializer_class = HabitsSerializer
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        return Habits.objects.filter(is_public=True)
