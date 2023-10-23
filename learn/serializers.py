from rest_framework import serializers

from learn.models import Course, Lesson, Payments, CourseSubscription
from learn.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    lesson_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.IntegerField(source='course.all.count', read_only=True)
    lesson = LessonSerializer(source='course', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return CourseSubscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['course_name', 'course_preview', 'course_comment',
                  'count_lesson', 'lesson', 'is_subscribed']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'


