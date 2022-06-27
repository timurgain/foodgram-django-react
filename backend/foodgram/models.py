from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    """Tag table."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
        unique=True,
    )
    color = ColorField(
        verbose_name='HEX-цвет тега',
        format='hex',
        default='#49B64E',
    )
    slug = models.SlugField(
        verbose_name='Удобочитаемая метка URL',
        unique=True,
        max_length=200,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Ожидается строка из цифр и букв'
            ),
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name[:30]


class TagInRecipe(models.Model):
    """Explicit table implementation
    of tags in recipes."""
    tag = models.ForeignKey(
        to='Tag',
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Тег в рецепте'
        verbose_name_plural = 'Теги в рецептах'


class Ingredient(models.Model):
    """Ingredient table."""
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
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self) -> str:
        return self.name[:30] + ' - ' + self.measurement_unit


class IngredientInRecipe(models.Model):
    """Explicit table implementation
    of ingredient with its quantity in recipe."""
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        to='Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Инградиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1, message='1 - минимальное количество'),
            MaxValueValidator(999, message='999 - максимальное количество'),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self) -> str:
        return (f"{self.ingredient.name}"
                f" - {self.amount} {self.ingredient.measurement_unit}")


class Recipe(models.Model):
    """Recipe table."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )
    tags = models.ManyToManyField(
        to='Tag',
        through='TagInRecipe',
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        to='users.User',
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
        ),
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
        ordering = ('-updated_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipename_author'
            ),
        )

    def __str__(self) -> str:
        return self.name[:30]


class FavoriteRecipe(models.Model):
    """Favorite recipes table."""
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        related_name='lovers',
        verbose_name='Рецепт',
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
        ordering = ('-updated_at',)
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_cant_add_in_favorite_recipe_twice'
            ),
        )

    def __str__(self) -> str:
        return f"Список избранных рецептов у пользователя {self.owner}"


class ShoppingCart(models.Model):
    """Shopping cart table."""
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
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
        ordering = ('-updated_at',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_cant_add_in_cart_recipe_twice'
            ),
        )

    def __str__(self) -> str:
        return f"Список покупок пользователя {self.owner}"
