from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

app_name = 'users'

# router.register(
#     prefix=r'users/subscriptions',
#     viewset=SubscriptionViewSet,
#     basename='subscriptions',
# )
# router.register(
#     prefix=r'users/(?P<user_id>\d+)/subscribe/',
#     viewset=SubscriptionViewSet,
#     basename='subscribe',
# )

# urlpatterns = [
#     path('', include(router.urls)),
# ]

router = DefaultRouter()
router.register(prefix=r'users', viewset=CustomUserViewSet)

urlpatterns = [
    # path('', include('djoser.urls')),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
