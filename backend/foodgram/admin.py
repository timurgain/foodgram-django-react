from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagInRecipe)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    paslist_display = ('id', 'name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('mame',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    paslist_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    search_fields = ('recipe', 'ingredient',)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1

    def get_queryset(self, request):
        queryset = super(IngredientInRecipeInline, self).get_queryset(request)
        queryset = queryset.filter(name=request.get('name'))
        return queryset


class TagInRecipeInline(admin.TabularInline):
    model = TagInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_favorite_count')
    readonly_fields = ('is_favorite_count',)
    list_filter = ('name', 'tags', 'author',)
    search_fields = ('name',)
    inlines = (IngredientInRecipeInline, TagInRecipeInline,)

    def is_favorite_count(self, obj):
        return obj.lovers.count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
