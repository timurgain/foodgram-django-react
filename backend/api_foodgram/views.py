from rest_framework.generics import get_object_or_404

from foodgram.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                             Tag)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from users.models import User

from api_foodgram.serializers import (ActionRecipeSerializer,
                                      FavoriteRecipeSerializer,
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

    def perform_update(self, serializer):
        serializer.save(
            ingredients=self.request.data['ingredients'],
            tags=self.request.data['tags']
        )

        @action(methods=['post', 'del'], detail=True,
                permission_classes=[permissions.IsAuthenticated])
        def favorite(self, request, id=None):
            user = self.request.user
            recipe = get_object_or_404(Recipe, id=id)
            favorite = ...


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    """."""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
