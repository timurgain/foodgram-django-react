from foodgram.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                             Tag)
from users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model in the foodgram app."""
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)


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
