import django_filters
from django_filters import widgets

from foodgram.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """Filter for Recipe model and additional fields not from the model
    and tags slug-field insted of name-field."""
    is_favorited = django_filters.BooleanFilter(
        method='is_favorited_filter',
        label='is_favorited',
        widget=widgets.BooleanWidget(),
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='is_in_shopping_cart_filter',
        label='is_in_shopping_cart',
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='tags',
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags',)

    def is_favorited_filter(self, queryset, name, value):
        if value:
            return queryset.filter(lovers__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset
