from foodgram.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                             Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import User

from api_foodgram.serializers import (ActionRecipeSerializer,
                                      FavoriteRecipeSerializer,
                                      IngredientSerializer,
                                      LiteRecipeSerializer,
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

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)  # не понятно, работает с pk
        favorite = FavoriteRecipe.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST' and favorite.exists():
            return Response(
                "Ошибка, этот рецепт уже есть в списке избранного.",
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'POST':
            new_favorite = FavoriteRecipe.objects.create(
                user=user, recipe=recipe)
            new_favorite.save()
            serializer = LiteRecipeSerializer(
                instance=recipe, context={'request': request})
            return Response(
                serializer.data
            )
        elif request.method == 'DELETE' and favorite.exists():
            favorite.delete()
            return Response(
                "Ок, рецепт удален из избранного.",
                status=status.HTTP_204_NO_CONTENT
            )
        elif request.method == 'DELETE':
            return Response(
                "Ошибка, рецепт не был в избранном.",
                status=status.HTTP_400_BAD_REQUEST
            )


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    """."""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
