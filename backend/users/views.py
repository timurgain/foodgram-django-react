from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from djoser.views import UserViewSet


# class CustomUserViewSet(UserViewSet):
#     """."""
#     pass
