from foodgram.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                             Tag)
from rest_framework import viewsets
from users.models import User

from api_foodgram.serializers import (ActionRecipeSerializer,
                                      FavoriteRecipesSerializer,
                                      IngredientSerializer,
                                      ReadRecipeSerializer,
                                      ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Tag model in the foodgram app."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """."""
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DEL'):
            return ActionRecipeSerializer
        return ReadRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            ingredients=self.request.data['ingredients'],
            tags=self.request.data['tags']
        )


class FavoriteRecipesViewSet(viewsets.ModelViewSet):
    """."""
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
