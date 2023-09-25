from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from learn.models import Course, Lesson
from users.models import User


class LessonTest(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'test@test.com', 'password': '12345'}
        self.user = User.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(course_name='Тест курс')

        self.lesson = Lesson.objects.create(
            lesson_name='Тест1 имя',
            lesson_comment='Тест1',
            lesson_url='https://www.youtube.com/',
            owner=self.user
        )

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

    def test_lesson_url_bad(self):
        data_lesson = {
            'course_name': self.course.pk,
            'lesson_name': 'Тест имя',
            'lesson_comment': 'Тест',
            'lesson_url': 'https://www.test.com',
            'owner': self.user.pk
        }
        response = self.client.post(reverse('learn:create'), data_lesson)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_detail(self):
        response = self.client.get(reverse('learn:detail', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        response = self.client.delete('/lesson/1/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
