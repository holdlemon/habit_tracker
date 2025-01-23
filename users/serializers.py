from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    ''' Сериализатор для пользователя '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Хешируем пароль с использованием set_password
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Хешируем пароль при обновлении, если пароль предоставлен
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserCommonSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя с ограниченным набором полей"""

    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Хешируем пароль с использованием set_password
        password = validated_data.pop("password", None)
        user = User(email=validated_data["email"])
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Хешируем пароль при обновлении, если пароль предоставлен
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)  # Хешируем пароль
            instance.save()  # Сохраняем изменения после установки пароля
        return super().update(instance, validated_data)
