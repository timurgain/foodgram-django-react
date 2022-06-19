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


# class TagInRecipeSerializer(serializers.ModelSerializer):
#     """Serializer for explicit TagInRecipe model in the foodgram app."""
#     id = serializers.IntegerField(source='tag.id')

#     class Meta:
#         model = TagInRecipe
#         fields = ('id', 'tag', 'recipe',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class ReadIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer shows an amount of ingredient in a recipe."""
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class ActionIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for adding ingredients while creating a recipe."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Serializer for get method on recipes in Recipe model."""
    tags = TagSerializer(read_only=True)
    ingredients = ReadIngredientInRecipeSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)


class ActionRecipeSerializer(serializers.ModelSerializer):
    """Serializer for post, patch, del methods on recipes in Recipe model."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = ActionIngredientInRecipeSerializer(many=True)
    author = CustomDjoserUserSerializer(read_only=True)
    image = Base64ToImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)

    def to_representation(self, instance):
        return super().to_representation(instance)

    def to_internal_value(self, data):
        """
        Здесь валидирую поля с типом nested serializer:
        - tags,
        - ingredients.

        Затем эти значения как-то добавятся к словарю validated_data после
         вызова метода perform_create во ViewSet.
        Валидация через методы validate_tags и validate_ingredients
         не получилась :(
        Еще вариант валидировать эти поля в самом методе create,
         но там кажется неуместно.
        """
        ingredients = []
        for ingredient in data['ingredients']:
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': 'Ожидается количество больше 0.'
                })
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не могут повторяться.'
                })
            ingredient_exists = (Ingredient.objects
                                 .filter(id=ingredient['id']).exists())
            if not ingredient_exists:
                raise serializers.ValidationError({
                    'ingredients': 'Используйте существующие ингредиенты.'
                })
            ingredients.append(ingredient['id'])

        for tag_id in data['tags']:
            tag_exists = Tag.objects.filter(id=tag_id).exists()
            if not tag_exists:
                raise serializers.ValidationError({
                    'tags': 'Используйте id существующих тегов.'
                })
        return super().to_internal_value(data)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            kwargs = {
                'recipe': recipe,
                'ingredient': Ingredient.objects.get(id=ingredient['id']),
                'amount': ingredient['amount'],
            }
            IngredientInRecipe.objects.create(**kwargs)
        for tag_id in tags:
            kwargs = {
                'recipe': recipe,
                'tag': Tag.objects.get(id=tag_id),
            }
            TagInRecipe.objects.create(**kwargs)
        return recipe

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
