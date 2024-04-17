from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User


class UserAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test1@test1.ru",
            chat_id="@telegram_test1",
            password='12345'
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        data = {
            "email": "test2@test2.ru",
            "chat_id": "@telegram_test2",
            "password": "12345"
        }
        response = self.client.post(
            reverse('users:users-list'),
            data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):

        response = self.client.delete(
            reverse('users:users-detail', args=[self.user.id])
            )

        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
