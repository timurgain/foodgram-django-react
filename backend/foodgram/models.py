from collections import namedtuple

from backend.users.models import User
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Tag(models.Model):
    """."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
        unique=True,
    )
    color = models.CharField(
        verbose_name='HEX-цвет тега',
        max_length=7,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Ожидается цветовой HEX-код, например, #49B64E'
            )
        )
    )
    slug = models.SlugField(
        verbose_name='Удобочитаемая метка URL',
        unique=True,
        max_length=200,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Ожидается строка из цифр и букв'
            )
        )
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name[:30]


class Ingredient(models.Model):
    """."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name[:30]


class Recipe(models.Model):
    """."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )
    tags = models.ManyToManyField(
        to='Tag',
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Инградиенты'
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipies/'
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(1, message='1 минута - минимальное значение'),
            MaxValueValidator(1440, message='1 день - максимальное значение'),
        )
    )
    created_at = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipename_author'
            )
        )

    def __str__(self) -> str:
        return self.name[:30]


class IngredientInRecipe(models.Model):  # <<< ! >>>
    """Ingredient table with its quantity."""
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        to='Ingredient',
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Инградиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        null=True,
        blank=True,
    )


class BaseFavoriteCart(models.Model):  # <<< ! >>>
    """."""
    owner = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец'
    )
    recipies = models.ManyToManyField(
        to='Recipe',
        related_name='+',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        ordering = ['-updated_at']
        abstract = True


class FavoriteRecipes(BaseFavoriteCart):

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'

    def __str__(self) -> str:
        return f"Список избранных рецептов от пользователя {self.owner}"


class ShoppingCart(BaseFavoriteCart):

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return f"Список покупок пользователя {self.owner}"
