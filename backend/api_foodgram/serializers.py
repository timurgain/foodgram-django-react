from foodgram.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                             Tag, TagInRecipe, IngredientInRecipe)
from users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model in the foodgram app."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('id', 'name', 'color', 'slug',)


class TagInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for explicit TagInRecipe model in the foodgram app."""

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
    tags = TagInRecipeSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


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
