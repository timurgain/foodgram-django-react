from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, TokenCreateSerializer, UserSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom serializer to create user via Djoser."""
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """Custom serializer for model User via Djoser."""

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            # 'is_subscribed',
        )


# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for model User."""

#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name',
#             # 'is_subscribed',
#         )


class CustomTokenCreateSerializer(TokenCreateSerializer):
    pass
