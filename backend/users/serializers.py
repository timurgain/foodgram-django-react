from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class CustomDjoserUserCreateSerializer(UserCreateSerializer):
    """Custom serializer to create user via Djoser."""
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomDjoserUserSerializer(UserSerializer):
    """Custom serializer for model User via Djoser."""

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            # 'is_subscribed',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for model User in case of subscriptions list request."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            # 'is_subscribed',
        )


class PostFollowSerializer(serializers.ModelSerializer):
    """Serializer for model Follow in case of POST subscription request.
    Used for input data validation."""

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='You are already following that user.',
            ),
        )

    def validate(self, attrs):
        request_user = self.context.get('request').user
        following_user = attrs.get('following')
        if request_user == following_user:
            raise serializers.ValidationError("You can't follow yourself.")
        return super().validate(attrs)
