from rest_framework import serializers

from foodgram.models import (FavoriteRecipe, Ingredient, IngredientInRecipe,
                             Recipe, ShoppingCart, Tag, TagInRecipe)
from users.serializers import CustomDjoserUserSerializer

from .fields import Base64ToImageField


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model in the foodgram app."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model in the foodgram app."""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class ReadIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer shows an ingredient with amount in a recipe."""
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


class LiteRecipeSerializer(serializers.ModelSerializer):
    """Serializer for response when adding a recipe to favorites."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe appearance."""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    author = CustomDjoserUserSerializer()

    class Meta:
        model = Recipe

        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        queryset = IngredientInRecipe.objects.filter(recipe=obj)
        serializer = ReadIngredientInRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        return self.is_in_model(self, obj, model=FavoriteRecipe)

    def get_is_in_shopping_cart(self, obj):
        return self.is_in_model(self, obj, model=ShoppingCart)

    @staticmethod
    def is_in_model(self, obj, model) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()


class ActionRecipeSerializer(serializers.ModelSerializer):
    """Serializer for post, patch methods on recipes, not for appearance."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = ActionIngredientInRecipeSerializer(many=True)
    author = CustomDjoserUserSerializer(read_only=True)
    image = Base64ToImageField()

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'author', 'ingredients',
                  'image', 'text', 'cooking_time',)

    def to_representation(self, instance):
        serializer = ReadRecipeSerializer(instance, context=self.context)
        return serializer.data

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
            if not Tag.objects.filter(id=tag_id).exists():
                raise serializers.ValidationError({
                    'tags': 'Используйте id существующих тегов.'
                })
        return super().to_internal_value(data)

    def create(self, validated_data):
        tags, ingredients = self.pop_tags_ingredients(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        self.tag_in_recipe_create(tags, recipe)
        self.ingredient_in_recipe_create(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags, ingredients = self.pop_tags_ingredients(validated_data)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        TagInRecipe.objects.filter(recipe=instance).delete()
        self.tag_in_recipe_create(tags, recipe=instance)
        self.ingredient_in_recipe_create(ingredients, recipe=instance)
        return super().update(instance, validated_data)

    @staticmethod
    def pop_tags_ingredients(validated_data: dict) -> tuple:
        return validated_data.pop('tags'), validated_data.pop('ingredients')

    @staticmethod
    def tag_in_recipe_create(tags: list, recipe: Recipe):
        for tag_id in tags:
            kwargs = {
                'recipe': recipe,
                'tag': Tag.objects.get(id=tag_id),
            }
            TagInRecipe.objects.create(**kwargs)

    @staticmethod
    def ingredient_in_recipe_create(ingredients: list, recipe: Recipe):
        for ingredient in ingredients:
            kwargs = {
                'recipe': recipe,
                'ingredient': Ingredient.objects.get(id=ingredient['id']),
                'amount': ingredient['amount'],
            }
            IngredientInRecipe.objects.create(**kwargs)
