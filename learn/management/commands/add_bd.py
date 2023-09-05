from django.core.management import BaseCommand

from learn.models import Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        customer = User.objects.get(email='vadimcola@mail.ru')

        Payments.objects.create(customer=customer, payment_date='2023-09-05',
                                paid_course_id=1, paid_lesson_id=None,
                                payment='17500', payment_method='cash')

