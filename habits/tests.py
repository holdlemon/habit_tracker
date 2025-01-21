from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from habits.models import Habits
from users.models import User


class HabitsTests(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email='user1@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем привычку для тестов
        self.habit = Habits.objects.create(
            user=self.user,
            place="В зале",
            time="20:00:00",
            action="Заниматься спортом",
            is_pleasant=False,
            periodicity=1,
            award=None,
            execution_time=60,
            is_public=False
        )

    def test_habits_create(self):
        """Тест создания привычки"""
        url = reverse('habits:habits_create')
        data = {
            "place": "Дома",
            "time": "12:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "periodicity": 1,
            "award": None,
            "execution_time": 60,
            "is_public": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), 2)

    def test_habits_update(self):
        """Тест обновления привычки"""
        url = reverse('habits:habits_update', args=[self.habit.id])
        data = {
            "action": "Бегать на улице"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Бегать на улице")

    def test_habits_delete(self):
        """Тест удаления привычки"""
        url = reverse('habits:habits_delete', args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.count(), 0)

    def test_habits_retrieve(self):
        """Тест получения одной привычки"""
        url = reverse('habits:habits_retrieve', args=[self.habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit.action)

    def test_habits_list(self):
        """Тест получения списка привычек"""
        url = reverse('habits:habits_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_habits_public_list(self):
        """Тест получения списка публичных привычек"""
        # Создаем публичную привычку
        public_habit = Habits.objects.create(
            user=self.user,
            place="Парк",
            time="18:00:00",
            action="Гулять",
            is_pleasant=False,
            periodicity=1,
            award=None,
            execution_time=60,
            is_public=True
        )
        url = reverse('habits:habits_public_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
