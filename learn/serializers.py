from rest_framework import serializers

from learn.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.IntegerField(source='course.all.count', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
