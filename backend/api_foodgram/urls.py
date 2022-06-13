from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, TagViewSet, RecipesViewSet

app_name = 'api_foodgram'

router_v1 = routers.DefaultRouter()

router_v1.register(
    prefix='tags', viewset=TagViewSet
)
router_v1.register(
    prefix='recipes', viewset=RecipesViewSet
)
router_v1.register(
    prefix='ingredients', viewset=IngredientViewSet, basename='ingredient'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
