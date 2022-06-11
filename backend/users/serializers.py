from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, TokenCreateSerializer
from .models import User
from djoser.conf import settings


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom serializer."""
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomTokenCreateSerializer(TokenCreateSerializer):
    pass
