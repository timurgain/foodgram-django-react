from django.urls import include, path, re_path
from rest_framework import routers
from backend.api_foodgram import views

app_name = 'api_foodgram'

router_v1 = routers.DefaultRouter()

# router_v1.register(
#     prefix=r'(?P<version>v1)/users',
#     viewset='',
# )

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
