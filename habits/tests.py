from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование привычек"""

    def setUp(self):

        self.user = User.objects.create(
            email="test1@test1.ru",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password("test")
        self.user.save()

        self.nice_habit = Habit.objects.create(
            owner= self.user,
            place= "None",
            time= "08:00",
            action= "Сьесть десерт",
            sign_of_pleasant= "True",
            periodicity= "7",
            time_to_complete= "0:01:30",
            is_published= "True"
        )

        self.good_habit = Habit.objects.create(
            owner= self.user,
            place= "Спортивная площадка",
            time= "11:00",
            action= "Пробежка",
            sign_of_pleasant= "False",
            periodicity= "2",
            reward="Отдых",
            time_to_complete= "0:01:30",
            is_published= "True"
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {
                "owner": self.user.pk,
                "place": "Спортивная площадка",
                "time": "10:10",
                "action": "Пробежка",
                "sign_of_pleasant": "False",
                "periodicity": "2",
                "related_habit": "1",
                "reward": "",
                "time_to_complete": "0:01:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_good_habit(self):
        """Тестирование вывода списка полезных привычек"""
        response = self.client.get(
            reverse('habits:good_habits-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [{'action': 'Пробежка',
                                                        'id': self.good_habit.id,
                                                        'is_published': True,
                                                        'owner': self.user.id,
                                                        'periodicity': 2,
                                                        'place': 'Спортивная площадка',
                                                        'related_habit': None,
                                                        'reward': 'Отдых',
                                                        'next_date': None,
                                                        'sign_of_pleasant': False,
                                                        'time': '11:00:00',
                                                        'time_to_complete': '00:01:30'}])

    def test_list_nice_habit(self):
        """Тестирование вывода списка приятных привычек"""
        response = self.client.get(
            reverse('habits:nice_habits-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [{'action': 'Сьесть десерт',
                                                        'id': self.nice_habit.id,
                                                        'is_published': True,
                                                        'owner': self.user.id,
                                                        'periodicity': 7,
                                                        'place': 'None',
                                                        'related_habit': None,
                                                        'reward': None,
                                                        'next_date': None,
                                                        'sign_of_pleasant': True,
                                                        'time': '08:00:00',
                                                        'time_to_complete': '00:01:30'}])

    def test_list_owner_habit(self):
        """Тестирование вывода списка привычек пользователя"""
        response = self.client.get(
            reverse('habits:owner_habits-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_habit(self):
        """Тестирование вывода одной привычки"""
        response = self.client.get(
            reverse('habits:habit-get', args=[self.nice_habit.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.nice_habit.action)

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        updated_data = {
            "action": "Updated habit",
            "sign_of_pleasant": "False",
            "periodicity": 7,
            "reward": "",
            "time_to_complete": "00:01:30",
            "related_habit": self.nice_habit.id
        }

        response = self.client.patch(
            reverse('habits:habit-update', args=[self.good_habit.id]), updated_data
        )

        self.nice_habit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], updated_data['action'])

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        response = self.client.delete(
            reverse('habits:habit-delete', args=[self.nice_habit.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.nice_habit.id).exists())


class HabitTestCaseValidationError(APITestCase):
    """Тестирование валидации при создании привычек"""

    def setUp(self):

        self.user = User.objects.create(
            email="test1@test1.ru",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password("test")
        self.user.save()

        self.nice_habit = Habit.objects.create(
            owner= self.user,
            place= "None",
            time= "08:00",
            action= "Сьесть десерт",
            sign_of_pleasant= "True",
            periodicity= "7",
            time_to_complete= "0:01:30",
            is_published= "True"
        )

        self.good_habit = Habit.objects.create(
            owner= self.user,
            place= "Спортивная площадка",
            time= "11:00",
            action= "Пробежка",
            sign_of_pleasant= "False",
            periodicity= "2",
            reward="Отдых",
            time_to_complete= "0:01:30",
            is_published= "True"
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit_with_related_habit_or_reward(self):
        """Тестирование создания привычки при одновременном указании награды и связанной привычки"""
        data = {
                "owner": self.user.id,
                "place": "Спортивная площадка",
                "time": "10:10",
                "action": "Пробежка",
                "sign_of_pleasant": "False",
                "periodicity": "2",
                "related_habit": self.nice_habit.id,
                "reward": "Отдых",
                "time_to_complete": "0:01:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Нельзя одновременно выбирать связанную привычку и указывать вознаграждение']})

    def test_create_habit_with_long_execution_time(self):
        """Тестирование создания привычки при указании времени выполнения больше 120 секунд"""
        data = {
                "owner": self.user.id,
                "place": "Спортивная площадка",
                "time": "10:10",
                "action": "Пробежка",
                "sign_of_pleasant": "False",
                "periodicity": "2",
                "related_habit": self.nice_habit.id,
                "reward": "",
                "time_to_complete": "0:02:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд']})

    def test_create_related_habit_with_pleasant(self):
        """Тестирование создания связанной привычки с признаком приятной"""
        data = {
                "owner": self.user.id,
                "place": "Спортивная площадка",
                "time": "10:10",
                "action": "Пробежка",
                "sign_of_pleasant": "False",
                "periodicity": "2",
                "related_habit": self.good_habit.id,
                "reward": "",
                "time_to_complete": "0:01:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['В связанные привычки могут попадать только привычки с признаком приятной привычки']})

    def test_create_pleasant_habit_with_reward_or_related(self):
        """Тестирование создания приятной привычки с вознаграждением или со связанной привычкой"""
        data = {
                "owner": self.user.id,
                "place": "None",
                "time": "10:10",
                "action": "Сьесть десерт",
                "sign_of_pleasant": "True",
                "periodicity": "2",
                "related_habit": "",
                "reward": "Отдых",
                "time_to_complete": "0:01:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки']})

    def test_create_habit_with_long_duration(self):
        """Тестирование создания привычки с периодом выполнения больше недели"""
        data = {
                "owner": self.user.id,
                "place": "Спортивная площадка",
                "time": "10:10",
                "action": "Пробежка",
                "sign_of_pleasant": "False",
                "periodicity": "9",
                "related_habit": "",
                "reward": "",
                "time_to_complete": "0:01:30",
                "is_published": "True"
            }

        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней']})
