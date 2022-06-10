from django.urls import include, path, re_path
from rest_framework import routers

from .views import IngredientViewSet

app_name = 'api_foodgram'

router_v1 = routers.DefaultRouter()

router_v1.register(
    prefix='ingredients', viewset=IngredientViewSet, basename='ingredient'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]

urlpatterns += [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
