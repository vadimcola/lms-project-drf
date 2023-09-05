from django.core.management import BaseCommand

from learn.models import Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        customer = User.objects.get(email='vadimcola1983@yandex.ru')

        Payments.objects.create(customer=customer, payment_date='2023-07-10',
                                paid_course_id=2, paid_lesson_id=7,
                                payment='11000', payment_method='cash')

