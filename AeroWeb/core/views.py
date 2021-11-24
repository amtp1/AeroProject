import os
import mimetypes
from json import dumps

from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.generics import ListAPIView

from .models import *
from .serializer import *

class UsersView(ListAPIView):
    serializer_class = UsersSerializer
    def get(self, request):
        queryset = Users.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return HttpResponse(dumps({"users": serializer.data}), content_type='application/json')

class UserRegistration(ListAPIView):
    serializers_class = UserRegistrationSerializer

    def get(self, request, last_name: str, first_name: str, middle_name: str, position: str, department: str, password: str):
        queryset = Users.objects.filter(last_name=last_name)
        if queryset.exists():
            return HttpResponse(dumps({"response": False}))
        else:
            Users.objects.create(last_name=last_name, first_name=first_name,
                    middle_name=middle_name, position=position,
                    department=department, password=password)
            return HttpResponse(dumps({"response": True}))

class UserLogin(ListAPIView):
    serializer_class = UserLoginSerializer

    def get(self, request, last_name: str, department: str, password: str):
        is_queryset = Users.objects.filter(last_name=last_name).exists()
        if is_queryset:
            queryset = Users.objects.filter(last_name=last_name, department=department, password=password).all()
            serializer = UserLoginSerializer(queryset, many=True)
            return HttpResponse(dumps({"user": serializer.data, "is_reg": is_queryset}), content_type='application/json')
        else:
            return HttpResponse(dumps({"user": [], "is_reg": is_queryset}), content_type='application/json')

class UserUpdateActive(ListAPIView):
    serializers_class = UserLoginSerializer

    def get(self, request, last_name: str, active: int):
        user = Users.objects.get(last_name=last_name)
        user.is_active = active
        user.save()
        return HttpResponse(True)

def index(request):
    return render(request, "index.html")

def download_file(request, filename="AeroSetupMain.exe"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define the full file path
    filepath = BASE_DIR + r'/core/media/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response