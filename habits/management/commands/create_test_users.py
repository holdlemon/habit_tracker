from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт двух тестовых пользователей'

    def handle(self, *args, **options):
        User = get_user_model()

        # Создание тестового юзера №1
        try:
            User.objects.get(email='user1@example.com').delete()
            self.stdout.write(self.style.WARNING(f"Пользователь с email 'user1@example.com' удалён."))
        except ObjectDoesNotExist:
            pass

        # Создаём первого пользователя
        user1 = User.objects.create(
            email='user1@example.com',
        )
        user1.set_password('testpass123')
        user1.save()
        self.stdout.write(self.style.SUCCESS(f'Пользователь {user1.email} создан.'))

        # Создание тестового юзера №2
        try:
            User.objects.get(email='user2@example.com').delete()
            self.stdout.write(self.style.WARNING(f"Пользователь с email 'user2@example.com' удалён."))
        except ObjectDoesNotExist:
            pass

        # Создаём второго пользователя
        user2 = User.objects.create(
            email='user2@example.com',
        )
        user2.set_password('testpass123')
        user2.save()
        self.stdout.write(self.style.SUCCESS(f'Пользователь {user2.email} создан.'))
