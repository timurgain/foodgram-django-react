import django_filters

from foodgram.models import Recipe, Ingredient, TagInRecipe


class RecipeFilter(django_filters.FilterSet):
    """filter for Recipe model and additional fields not from the model."""
    is_favorited = django_filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = django_filters.BooleanFilter(method='')
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags',)

        def is_favorited_filter(self, queryset, name, value):
            pass

        def is_in_shopping_cart_filter(self, queryset, name, value):
            pass
