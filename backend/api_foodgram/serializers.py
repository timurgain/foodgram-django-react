from foodgram.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                             Tag, TagInRecipe, IngredientInRecipe)
from users.models import User
from users.serializers import CustomDjoserUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .fields import Base64ToImageField


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model in the foodgram app."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('id', 'name', 'color', 'slug',)


class TagInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for explicit TagInRecipe model in the foodgram app."""
    id = serializers.IntegerField(source='tag.id')

    class Meta:
        model = TagInRecipe
        fields = ('id', 'tags', 'recipies',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for explicit IngredientInRecipe model in the foodgram app."""

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'recipe', 'ingredient', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model in the foodgram app."""
    tags = TagInRecipeSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True)
    author = CustomDjoserUserSerializer(read_only=True)
    image = Base64ToImageField()

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)

    def create(self, validated_data):
        # ingredients_data = validated_data.pop('ingredients')
        # tags_data = validated_data.pop('tags')
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_ingredients(self, value):
        ingredients = []
        for ingredient in value:
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError(
                    'Ожидается количество больше 0.'
                )
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться.'
                )
            ingredients.append(ingredient['id'])
            return value
        
    def validate_tags(self, value):
        for tag in value:
            pass







class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """Serializer for FavoriteRecipes model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('owner', 'recipies')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for ShoppingCart model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('owner', 'recipies')
