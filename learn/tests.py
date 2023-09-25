from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from learn.models import Course
from users.models import User


class LessonTest(APITestCase):
    # email = 'test@tast.com'
    # password = '12345'

    def setUp(self):
        # self.user = User.objects.create(
        #     email=self.email
        # )
        # self.user.set_password(self.password)
        # self.user.save()
        #
        # response = self.client.post(
        #     '/api/token/',
        #     {
        #         'email': self.email,
        #         'password': self.password
        #     }
        # )
        #
        # self.token = response.json().get('access')
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.user_data = {'email': 'test@test.com', 'password': '12345'}
        self.user = User.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(course_name='Тест курс')

    def test_lesson_create(self):
        data_lesson = {
            'course_name': self.course.pk,
            'lesson_name': 'Тест имя',
            'lesson_comment': 'Тест',
            'lesson_url': 'https://www.youtube.com/',
            'owner': self.user.pk
        }
        response = self.client.post(reverse('learn:create'), data_lesson)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
