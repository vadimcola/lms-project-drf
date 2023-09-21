from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learn.models import Lesson
from users.models import User


class LessonListTest(APITestCase):
    def SetUp(self):
        self.user = User.objects.create(
            email='test@tast.com',
            password='12345'
        )
        self.client.force_authenticate(user=self.user)
        self.name = Lesson.objects.create(
            lesson_name="Тест",
            lesson_url="https://www.youtube.com/",
            owner=self.user

        )

    def test_get_list(self):
        response = self.client.get(reverse('learn:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

