from django.contrib.auth.models import User

from django.urls import reverse
from psycopg2 import DATETIME
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Tracker
from employees.models import Employee

from datetime import date, datetime

TRACKER_DATETIME = date.today()
TRACKER_DATETIME_STR = date.today().strftime('%Y-%m-%dT00:00:00Z')

class TrackerTest(APITestCase):
    """ Тест модели TRACKER """

    def setUp(self):
        """ Исходные данные """

        Employee.objects.all().delete()
        Tracker.objects.all().delete()

        # Создаем модели сотрудника и задачи
        self.user = User.objects.create(username='test')
        self.employee = Employee.objects.create(name='Новый сотрудник')
        self.tracker = Tracker.objects.create(title='Test', description='test', deadline=TRACKER_DATETIME)
        self.client.force_authenticate(user=self.user)

    def test_tracker_create(self):
        """ Тестирование создание задачи """

        data = {
            'title': 'TEST',
            'description': 'test',
            'deadline': TRACKER_DATETIME,
            'status': 'active',
            'employee': self.employee.id,
        }
        response = self.client.post(
            '/tracker/trackers/',
            data=data
        )
        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'TEST', 'description':'test', 'deadline': TRACKER_DATETIME_STR, 'status': 'active', 'parent': None,
             'employee': 1}
        )

    def test_tracker_list(self):
        """ Тест списка всех задач """

        url = reverse('trackers:trackers-list')
        response = self.client.get(url)
        data = response.json()

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            [{'id': 1, 'title': 'Test', 'description': 'test','deadline': TRACKER_DATETIME_STR, 'status': 'consideration',
              'parent': None, 'employee': None}]
        )
        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            1
        )

    def test_tracker_retrieve(self):
        """ Тест детальной информации по задаче """

        url = reverse('trackers:trackers-detail', args=(self.tracker.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {'id': self.tracker.id, 'title': 'Test', 'description': 'test', 'deadline': TRACKER_DATETIME_STR, 'status': 'consideration',
             'parent': None, 'employee': None}
        )

    def test_tracker_update(self):
        """ Тестирование обновление задачи """

        url = reverse("trackers:trackers-detail", args=(self.tracker.pk,))

        data = {
            'employee': [self.employee.id],
            'status': 'active',
            'deadline': TRACKER_DATETIME,
            'title': 'TEST',
            'description': 'test',
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            1
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json()["status"], 'active')

    def test_tracker_update_parent(self):
        """ Тестирование обновление задачи """

        url = reverse("trackers:trackers-detail", args=(self.tracker.pk,))

        data = {
            'employee': [self.employee.id],
            'parent': [self.tracker.id],
            'status': 'active',
            'deadline': TRACKER_DATETIME,
            'title': 'TEST',
            'description': 'test',
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_tracker_delete(self):
        """ Тестирование удаление задачи """

        url = reverse("trackers:trackers-detail", args=(self.tracker.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем ожидаемое количество задач
        self.assertEqual(
            Tracker.objects.count(),
            0
        )
