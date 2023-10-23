from celery import shared_task
from django.core.mail import send_mail
from config import settings
from learn.models import CourseSubscription


@shared_task
def send_course_update(course_pk):
    course_list = CourseSubscription.objects.filter(course_id=course_pk)
    for course_item in course_list:
        send_mail(
            subject=f'Обновление курса {course_item.course.course_name}',
            message=f'Обновление курса {course_item.course.course_name}',
            recipient_list=[course_item.user.email],
            from_email=settings.EMAIL_HOST_USER)
    print("Сообщение отправлено")
