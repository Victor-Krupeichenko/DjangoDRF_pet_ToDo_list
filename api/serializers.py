from rest_framework import serializers
from todo_list.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializator(serializers.ModelSerializer):
    """Serializator model User"""

    class Meta:
        model = User
        fields = ["username"]


class TaskSerializer(serializers.ModelSerializer):
    """Serializator model Task"""
    user = UserSerializator()

    class Meta:
        model = Task
        fields = ["user", "title", "description", "date_create", "execute_status"]


class RegisterUserSerializator(serializers.Serializer):
    """Register User"""
    username = serializers.CharField(min_length=3, max_length=35, write_only=True, required=True)
    password1 = serializers.CharField(min_length=8, write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(min_length=8, write_only=True, required=True, validators=[validate_password])

    def validate(self, attrs):
        """Проверка полей"""
        if User.objects.filter(username=attrs.get("username")).exists():
            raise serializers.ValidationError(f"User: {attrs.get('username')} Already exists")
        if attrs.get("password1") != attrs.get("password2"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        """Создание пользователя"""
        user = User.objects.create(username=validated_data.get("username"))
        user.set_password(validated_data.get("password1"))
        user.save()
        return validated_data


class LoginUserSerializator(serializers.Serializer):
    """Login User"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        """Валидация поля username"""
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"User: {value} not found")
        return value
