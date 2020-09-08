from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase


class CallAPITests(APITestCase):
    url = "/api/chatterbot/"

    # post
    def test_post(self):
        # message yang benar
        response = self.client.post(self.url, {"text": "Bagaimana kabar mu?"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # message yang salah
        response = self.client.post(self.url, {"text": "abc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['response'], 'Maaf, aku gak ngerti')

    # get api name
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Chatbot API')
