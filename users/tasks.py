from users.models import User
from datetime import timedelta
from django.utils import timezone


def check_user():
    user_list = User.objects.all().filter(is_active=True)
    for user_items in user_list:
        one_month_ago = timezone.now()-timedelta(days=30)
        if user_items.last_login < one_month_ago:
            user_items.is_active = False
            user_items.save()


