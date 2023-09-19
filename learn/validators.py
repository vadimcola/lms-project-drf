import re

from rest_framework import serializers


def validate_url(value):
    pattern = r'(https?://)?(www\.)?youtube\.com'
    if not re.search(pattern, value):
        raise serializers.ValidationError("Содержимое содержит недопустимые ссылки.")
    return value
