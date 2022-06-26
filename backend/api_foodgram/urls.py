from django.urls import include, path

from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api_foodgram'

router_v1 = routers.DefaultRouter()

router_v1.register(
    prefix='tags', viewset=TagViewSet, basename='tags'
)
router_v1.register(
    prefix='recipes', viewset=RecipeViewSet, basename='recipes'
)
router_v1.register(
    prefix='ingredients', viewset=IngredientViewSet, basename='ingredients'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
