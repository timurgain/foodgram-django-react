from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from foodgram.models import Recipe

from .models import Follow

# from api_foodgram.serializers import ReadRecipeSerializer


class CustomDjoserUserCreateSerializer(UserCreateSerializer):
    """Custom serializer to create user via Djoser."""
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomDjoserUserSerializer(UserSerializer):
    """Custom serializer for model User via Djoser."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
            'recipes',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        author_recipes = obj.recipes.all()
        if recipes_limit:
            return LiteRecipeSerializer(
                instance=author_recipes[:int(recipes_limit)], many=True).data
        return LiteRecipeSerializer(
            instance=author_recipes, many=True).data


class LiteRecipeSerializer(serializers.ModelSerializer):
    """Serializer for response when adding a recipe to favorites."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


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
