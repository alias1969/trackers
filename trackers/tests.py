from datetime import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Tracker
from employees.models import Employee

from datetime import date



class TrackerTest(APITestCase):
    """ Тест модели TRACKER """

    def setUp(self):
        """ Исходные данные """

        Employee.objects.all().delete()
        Tracker.objects.all().delete()

        # Создаем модели сотрудника и задачи
        self.employee = Employee.objects.create(name='Новый сотрудник')
        self.tracker = Tracker.objects.create(title='Test', description='test', deadline=date.today())

    def test_tracker_create(self):
        """ Тестирование создание задачи """

        data = {
            'title': 'TEST',
            'description': 'test',
            'deadline': date.today(),
            'status': 'active',
            'employee': self.employee.id,
        }
        response = self.client.post(
            '/tracker/',
            data=data
        )

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'TEST', 'description':'test', 'deadline': date.today(), 'status': 'active', 'parent': None,
             'employee': [1]}
        )

    def test_tracker_list(self):
        """ Тест списка всех задач """

        url = reverse('trackers:trackers-list')
        response = self.client.get(url)
        data = response.json()

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            [{'id': 2, 'title': 'Test', 'description': 'test','deadline': date.today(), 'status': 'consideration',
              'parent': None, 'employee': []}]
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
            {'id': self.tracker.id, 'title': 'Test', 'description': 'test', 'deadline': date.today(), 'status': 'consideration',
             'parent': None, 'employee': []}
        )

    def test_tracker_update(self):
        """ Тестирование обновление задачи """

        url = reverse("trackers:trackers-detail", args=(self.tracker.pk,))

        data = {
            'employee': [self.employee.id],
            'parent': [self.tracker.id],
            'status': 'active',
            'deadline': date.today(),
            'title': 'TEST',
            'description': 'test',
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            1
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json()["status"], 'consideration')

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
