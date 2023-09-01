from django.core.management import BaseCommand

from learn.models import Payments


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payments.objects.create(customer=None, payment_date='2023-08-15',
                                paid_course_id=1, paid_lesson_id=1,
                                payment='12500', payment_method='cash')

