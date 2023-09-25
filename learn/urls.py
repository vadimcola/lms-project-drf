from rest_framework import routers
from django.urls import path
from learn.apps import LearnConfig
from learn.views import LessonList, LessonDetail, LessonCreate, LessonUpdate, LessonDelete, PaymentsList, \
    CourseSubscriptionCreate, CourseSubscriptionDelete, CourseViewSet

app_name = LearnConfig.name

urlpatterns = [
    path('lesson/', LessonList.as_view(), name='list'),
    path('lesson/<int:pk>/', LessonDetail.as_view()),
    path('lesson/create/', LessonCreate.as_view(), name='create'),
    path('lesson/<int:pk>/update/', LessonUpdate.as_view()),
    path('lesson/<int:pk>/delete/', LessonDelete.as_view()),
    path('payments/', PaymentsList.as_view()),
    path('subscribe/', CourseSubscriptionCreate.as_view()),
    path('subscribe/<int:pk>/delete/', CourseSubscriptionDelete.as_view()),

]

router = routers. SimpleRouter()
router.register('course', CourseViewSet)
urlpatterns += router.urls

