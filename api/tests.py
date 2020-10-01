from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Task, User


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        self.alter_user = User.objects.create_user(
            username='alter_user',
            password='12345'
        )
        self.user = User.objects.create_user(
            username='test_user',
            password='12345'
        )
        self.password = '12345'
        Task.objects.create(author=self.user, title='test_task_1',
                            description='task for testing',
                            status='NW', finish_date='2020-10-01')
        Task.objects.create(author=self.user, title='test_task_2',
                            description='task for testing',
                            status='NW', finish_date='2020-10-01')

        self.task = Task.objects.create(author=self.user, title='test_task',
                                        description='task for testing',
                                        status='NW', finish_date='2020-10-01')

    def test_registration_user(self):
        new_user = {
            'username': 'test_user_new',
            'password': 'test_user'
        }
        responce_registration = self.client.post(reverse('registration'),
                                                 new_user)
        self.assertEqual(responce_registration.status_code, 201,
                         msg='Problems with creating user')
        responce_registration = self.client.post(reverse('registration'),
                                                 new_user)
        self.assertEqual(responce_registration.status_code, 200,
                         msg='Creating users with equal names')
        responce_registration = self.client.post(reverse('registration'),
                                                 {'username': 'fail'})
        self.assertEqual(responce_registration.status_code, 400,
                         msg='Problems with parametrs with registration')

    def test_auth(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }
        responce_auth = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(responce_auth.status_code, 200,
                         msg='Problem with auth')
        self.assertTrue(responce_auth.data['access'], msg='Token problem')

    def test_task_get(self):
        """
        Test no auth task all/single.
        """
        responce = self.client.get('/api/v1/tasks/')
        self.assertEqual(responce.status_code, 401,
                         msg="Not auth users can't accese tasks!")
        responce = self.client.get('/api/v1/tasks/1/')
        self.assertEqual(responce.status_code, 401,
                         msg="Not auth users can't accese tasks!")
        """
        Test user tasks singl and all.
        """
        self.api_client.force_authenticate(user=self.user)
        responce = self.api_client.get('/api/v1/tasks/')
        self.assertEqual(responce.status_code, 200,
                         msg='Problems with acces own tasks')
        self.assertContains(responce, self.task)
        responce = self.api_client.get('/api/v1/tasks/1/')
        self.assertEqual(responce.status_code, 200,
                         msg='Problems with acces own task')
        self.assertContains(responce, self.task)
        """
        Test access to others tasks.
        """
        self.api_client.force_authenticate(user=self.alter_user)
        responce = self.api_client.get('/api/v1/tasks/')
        self.assertEqual(len(responce.data), 0,
                         msg='Another users can see your tasks')
        responce = self.api_client.get('/api/v1/tasks/1/')
        self.assertEqual(responce.status_code, 404,
                         msg='Another users can see your task')

    def test_create_task(self):
        new_task = {
            'author': self.user,
            'title': 'test_new',
            'description': 'new test task',
            'status': 'DN',
        }
        self.api_client.force_authenticate(user=self.user)
        url = '/api/v1/tasks/'
        responce = self.api_client.post(url, new_task)
        self.assertEqual(responce.status_code, 201)

    def test_alter_task(self):
        alter_task = {
            'title': 'alter_title',
            'description': 'alter task',
            'status': 'DN',
            'finish_date': '2021-01-01',
        }
        self.api_client.force_authenticate(user=self.user)
        url = '/api/v1/tasks/1/'
        responce = self.api_client.get(url)
        self.assertNotContains(responce, alter_task)
        responce = self.api_client.patch(url, alter_task)
        self.assertContains(responce, 'alter_title')
        responce = self.api_client.delete('/api/v1/tasks/2/')
        self.assertEqual(responce.status_code, 204)
        responce = self.api_client.get('/api/v1/tasks/2/')
        self.assertEqual(responce.status_code, 404)

    def test_history(self):
        alter_task = {
            'title': 'history_title',
            'description': 'history task',
            'status': 'IW',
            'finish_date': '2022-01-01',
        }

        data = {
            'username': self.user.username,
            'password': self.password,
        }

        responce_auth = self.client.post(reverse('token_obtain_pair'), data)
        token = responce_auth.data['access']
        url = '/api/v1/history/1/'
        """
        Test adding history whel altered task.
        """
        responce = self.client.get(
            url, {},
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
            )
        len_old = len(responce.data)
        self.api_client.force_authenticate(user=self.user)
        self.api_client.patch('/api/v1/tasks/1/', alter_task)
        responce = self.client.get(
            url, {},
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
            )
        len_new = len(responce.data)
        self.assertContains(responce, 'history_title')
        self.assertEqual(len_new-1, len_old)
        """
        Check that user can't edit HistoryTask table.
        """
        responce = self.client.post(
            url, {},
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
            )
        self.assertEqual(responce.status_code, 405)
        responce = self.client.patch(
            url, {},
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
            )
        self.assertEqual(responce.status_code, 405)
        """
        Check that if user deleted task, history will be deleted too .
        """
        self.api_client.force_authenticate(user=self.user)
        responce = self.api_client.delete('/api/v1/tasks/1/')
        self.assertEqual(responce.status_code, 204)
        responce = self.client.get(
            url, {},
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
            )
        self.assertEqual(responce.status_code, 404)
