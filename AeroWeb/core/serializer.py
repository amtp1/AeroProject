from .models import *
from rest_framework import serializers

class UsersSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    middle_name = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    created = serializers.DateTimeField()
    is_active = serializers.BooleanField(default=False)

    class Meta:
        model = Users
        fields = ["last_name"]

class UserLoginSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    middle_name = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)
    created = serializers.DateTimeField()

    class Meta:
        model = Users
        fields = ["last_name", "department", "password"]

class UserRegistrationSerializer(serializers.Serializer):
    class Meta:
        model = Users

class ErrorNotify(serializers.Serializer):
    class Meta:
        model = NotifyError
