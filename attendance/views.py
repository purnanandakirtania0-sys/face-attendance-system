from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .models import Student

import base64
import uuid
import os


def login_page(request):
    return render(request, 'login.html')


def home_page(request):
    return render(request, 'home.html')


def attendance_page(request):
    return render(request, 'attendance.html')


def train_page(request):
    return render(request, 'train.html')


def dashboard_page(request):

    students = Student.objects.all()

    return render(request, 'dashboard.html', {
        'students': students
    })


def register_face(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        image_data = request.POST.get('image')

        if not image_data:

            messages.error(request, 'Camera image not found')

            return redirect('register_face')

        try:

            format, imgstr = image_data.split(';base64,')

            image_bytes = base64.b64decode(imgstr)

            filename = f"{uuid.uuid4()}.png"

            filepath = os.path.join(
                settings.MEDIA_ROOT,
                filename
            )

            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            Student.objects.create(
                name=name,
                dob=dob,
                email=email,
                image=filename
            )

            messages.success(
                request,
                'Student Registered Successfully'
            )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

        return redirect('register_face')

    return render(request, 'register.html')