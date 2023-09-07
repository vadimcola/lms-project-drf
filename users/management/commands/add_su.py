from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@test.ru',
            first_name='Иван',
            last_name='Иванов',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password('12345')
        user.save()
