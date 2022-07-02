# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
from django.core.management.base import BaseCommand, CommandError
from foodgram.models import Ingredient


class Command(BaseCommand):
    pass
