from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания суперпользователя"""

    help = "Создаёт суперпользователя с указанным email и паролем или создает с базовыми данными"

    def add_arguments(self, parser):
        # Добавляем аргументы для email и пароля
        parser.add_argument(
            "--email",
            type=str,
            default="admin@admin.ru",
            help="Email суперпользователя (по умолчанию: admin@admin.ru)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="123456qwerty",
            help="Пароль суперпользователя (по умолчанию: 123456qwerty)",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        email = options["email"]
        password = options["password"]

        # Удаляем существующего пользователя с таким email, если он есть
        try:
            User.objects.get(email=email).delete()
            self.stdout.write(self.style.WARNING(f"Пользователь с email {email} удалён."))
        except ObjectDoesNotExist:
            pass

        # Создаём нового суперпользователя
        user = User.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создан суперпользователь с email {user.email}")
        )
