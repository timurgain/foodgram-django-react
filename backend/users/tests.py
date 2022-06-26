from django.test import TestCase
from django.test.client import Client


class TestUsersViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_smth(self):
        pass
