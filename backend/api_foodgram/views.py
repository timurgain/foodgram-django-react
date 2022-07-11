from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api_foodgram.serializers import (ActionRecipeSerializer,
                                      IngredientSerializer,
                                      LiteRecipeSerializer,
                                      ReadRecipeSerializer, TagSerializer)
from foodgram.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                             Tag)

from .filters import RecipeFilter, IngredientSearchFilter
from .permissions import IsAuthorOrReadonly
from .services import get_ingredients_from_shopping_cart, get_shopping_file_pdf


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Tag model in the foodgram app."""
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Ingredient model in the foodgram app."""
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipe model in the foodgram app."""
    permission_classes = (IsAuthorOrReadonly,)
    queryset = Recipe.objects.all()
    filter_class = RecipeFilter
    filterset_fields = ('is_favorited', 'is_in_shopping_cart',
                        'author', 'tags')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
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

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.post_recipe_in_selected_model(
            request=request, model=FavoriteRecipe, pk=pk)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk=None):
        return self.delete_recipe_from_selected_model(
            request=request, model=FavoriteRecipe, pk=pk
        )

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.post_recipe_in_selected_model(
            request=request, model=ShoppingCart, pk=pk
        )

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk=None):
        return self.delete_recipe_from_selected_model(
            request=request, model=ShoppingCart, pk=pk
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = get_ingredients_from_shopping_cart(request)
        return get_shopping_file_pdf(ingredients)

    @staticmethod
    def post_recipe_in_selected_model(request, model, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe_in_selected_model = model.objects.filter(
            user=user, recipe=recipe)

        if recipe_in_selected_model.exists():
            return Response(
                "Ошибка, этот рецепт уже есть в списке.",
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            model.objects.create(user=user, recipe=recipe)
            serializer = LiteRecipeSerializer(
                instance=recipe, context={'request': request})
            return Response(
                serializer.data
            )

    @staticmethod
    def delete_recipe_from_selected_model(request, model, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe_in_selected_model = get_object_or_404(
            model, user=user, recipe=recipe)
        recipe_in_selected_model.delete()
        return Response(
            "Ок, рецепт удален из списка.",
            status=status.HTTP_204_NO_CONTENT
        )
