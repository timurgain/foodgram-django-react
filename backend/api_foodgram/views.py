from foodgram.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                             Tag)
from rest_framework import viewsets
from users.models import User

from api_foodgram.serializers import (FavoriteRecipesSerializer,
                                      IngredientSerializer, RecipeSerializer,
                                      ShoppingCartSerializer, TagSerializer,
                                      UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    """."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteRecipesViewSet(viewsets.ModelViewSet):
    """."""
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
