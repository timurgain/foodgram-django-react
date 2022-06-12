from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subscription, User


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


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for model Subscription."""
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Subscription
        fields = ('user', 'following',)

        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
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
