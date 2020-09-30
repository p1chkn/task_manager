from django.test import TestCase, Client
from django.urls import reverse
from .models impotr Task, HistoryTask


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        
