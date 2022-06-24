from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api_foodgram.serializers import (ActionRecipeSerializer,
                                      IngredientSerializer,
                                      LiteRecipeSerializer,
                                      ReadRecipeSerializer, TagSerializer)
from foodgram.models import (FavoriteRecipe, Ingredient, IngredientInRecipe,
                             Recipe, ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Tag model in the foodgram app."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Ingredient model in the foodgram app."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipe model in the foodgram app."""
    queryset = Recipe.objects.all()
    filterset_fields = [
        'is_favorited', 'is_in_shopping_cart', 'author', 'tags']

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
        ingredients = dict()
        recipes = Recipe.objects.filter(carts__user=request.user)

        for recipe in recipes:
            ingredients_in_recipe = (IngredientInRecipe.objects
                                     .filter(recipe=recipe))

            for obj in ingredients_in_recipe:
                if obj.ingredient.name in ingredients:
                    ingredients[obj.ingredient.name][0] += obj.amount
                else:
                    ingredients.update({
                        obj.ingredient.name: [obj.amount,
                                              obj.ingredient.measurement_unit]
                    })

        shopping_file = ''
        for key, value in ingredients.items():
            shopping_file += f"{key} - {value[0]} {value[1]}\n"
        response = HttpResponse(content=shopping_file,
                                content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_file.txt"')
        return response

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
