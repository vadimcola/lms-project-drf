from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from learn.models import Course, Lesson, CourseSubscription
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
            owner=self.user,
            course_name=self.course

        )

    def test_lesson_create(self):
        data_lesson = {
            'course_name': self.course.pk,
            'lesson_name': 'Тест имя',
            'lesson_comment': 'Тест',
            'lesson_url': 'https://www.youtube.com/',
            'owner': self.user.pk
        }
        response = self.client.post(reverse('learn:create'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_url_bad(self):
        data_lesson = {
            'course_name': self.course.pk,
            'lesson_name': 'Тест имя',
            'lesson_comment': 'Тест',
            'lesson_url': 'https://www.test.com',
            'owner': self.user.pk
        }
        response = self.client.post(reverse('learn:create'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_detail(self):
        response = self.client.get(reverse('learn:detail', args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "id": 1,
            "lesson_url": "https://www.youtube.com/",
            "lesson_name": "Тест1 имя",
            "lesson_preview": None,
            "lesson_comment": "Тест1",
            "course_name": self.course.pk,
            "owner": self.user.pk
        }
                         )

    def test_lesson_delete(self):
        response = self.client.delete('/lesson/1/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_update(self):
        data = {
            "lesson_name": "Тест измененный",
            "lesson_comment": "Измененный"
        }

        response = self.client.patch(reverse('learn:update', args=[self.lesson.pk]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "id": 1,
            "lesson_url": "https://www.youtube.com/",
            "lesson_name": "Тест измененный",
            "lesson_preview": None,
            "lesson_comment": "Измененный",
            "course_name": self.course.pk,
            "owner": self.user.pk
        }
                         )

    def test_lesson_list(self):
        response = self.client.get(reverse('learn:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "lesson_url": "https://www.youtube.com/",
                    "lesson_name": "Тест1 имя",
                    "lesson_preview": None,
                    "lesson_comment": "Тест1",
                    "course_name": self.course.pk,
                    "owner": self.user.pk
                },
            ],
        })


class CourseSubscriptionTest(APITestCase):
    def setUp(self):
        self.user_data = {'email': 'test@test.com', 'password': '12345'}
        self.user = User.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(course_name='Тест курс')

        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribed=True
        )

    def test_subscription_create(self):

        data_sub = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': True
        }
        response = self.client.post(reverse('learn:sub_create'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        response = self.client.delete('/subscribe/1/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
