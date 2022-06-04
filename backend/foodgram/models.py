from django.db import models


class Tag(models.Model):
    """."""
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название'
    )

    color = ...

    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Удобочитаемая метка URL',
    )

    class Meta:
        ordering = ['']
        verbose_name = ''
        verbose_name_plural = ''

    def str(self):
        return self.name[:30]


class Ingredient(models.Model):
    """."""
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название'
    )

    measurement_unit = ...

    class Meta:
        ordering = ['']
        verbose_name = ''
        verbose_name_plural = ''

    def str(self):
        return self.name[:30]


class Recipe(models.Model):
    """."""
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название'
    )

    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Удобочитаемая метка URL',
    )

    tags = ...

    author = ...

    ingredients = ...

    image = ...

    text = ...

    cooking_time = ...

    class Meta:
        ordering = ['']
        verbose_name = ''
        verbose_name_plural = ''

    def str(self):
        return self.name[:30]


class ShoppingCart(models.Model):
    """."""
    
    class Meta:
        ordering = ['']
        verbose_name = ''
        verbose_name_plural = ''

    def str(self):
        return 'Shopping_cart'
