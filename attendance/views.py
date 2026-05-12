from django.shortcuts import render, redirect
from django.contrib import messages
import subprocess
import os
import csv

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# ---------------- HOME PAGE ----------------

def home(request):

    if not request.session.get('user'):

        return redirect('login')

    return render(
        request,
        'home.html'
    )

# ---------------- LOGIN ----------------

def login_page(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # CHANGE YOUR LOGIN EMAIL & PASSWORD
        if email == "admin@gmail.com" and password == "1234":

            request.session['user'] = email

            return redirect('home')

        else:

            messages.error(
                request,
                "Invalid Email or Password"
            )

    return render(
        request,
        'login.html'
    )

# ---------------- REGISTER FACE ----------------

def register_face(request):

    if not request.session.get('user'):

        return redirect('login')

    if request.method == "POST":

        name = request.POST.get("name")
        student_id = request.POST.get("id")
        email = request.POST.get("email")

        # ---------------- CHECK DUPLICATE ----------------

        student_exists = False

        if os.path.exists("students.txt"):

            with open("students.txt", "r") as f:

                for line in f:

                    data = line.strip().split(",")

                    if len(data) >= 2:

                        old_id = data[1]

                        if old_id == student_id:

                            student_exists = True
                            break

        # ---------------- SAVE STUDENT ----------------

        if not student_exists:

            with open("students.txt", "a") as f:

                f.write(
                    f"{name},{student_id},{email}\n"
                )

        # ---------------- RUN DATASET SCRIPT ----------------

        script_path = os.path.join(
            BASE_DIR,
            'phase3_dataset_collection.py'
        )

        subprocess.run([
            'python',
            script_path,
            name
        ])

        messages.success(
            request,
            "Face Registered Successfully"
        )

        return redirect('train_page')

    return render(
        request,
        'register.html'
    )

# ---------------- TRAIN PAGE ----------------

def train_page(request):

    if not request.session.get('user'):

        return redirect('login')

    students = []

    dataset_path = os.path.join(
        BASE_DIR,
        "dataset"
    )

    if os.path.exists("students.txt"):

        unique_students = []

        with open("students.txt", "r") as f:

            lines = f.readlines()

            for line in lines:

                data = line.strip().split(",")

                if len(data) >= 3:

                    if data not in unique_students:

                        unique_students.append(data)

        for data in unique_students:

            name = data[0]
            student_id = data[1]
            email = data[2]

            image_name = ""

            for file in os.listdir(dataset_path):

                if (
                    file.endswith(".jpg")
                    and f".{name}." in file
                ):

                    image_name = file
                    break

            students.append({

                "name": name,
                "id": student_id,
                "email": email,
                "image": image_name

            })

    return render(
        request,
        'train.html',
        {
            'students': students
        }
    )

# ---------------- TRAIN MODEL ----------------

def train_model(request):

    if not request.session.get('user'):

        return redirect('login')

    script_path = os.path.join(
        BASE_DIR,
        'phase4_train_model.py'
    )

    subprocess.run([
        'python',
        script_path
    ])

    messages.success(
        request,
        "Model Trained Successfully"
    )

    return redirect('attendance_page')

# ---------------- ATTENDANCE PAGE ----------------

def attendance_page(request):

    if not request.session.get('user'):

        return redirect('login')

    return render(
        request,
        'attendance.html'
    )

# ---------------- START ATTENDANCE ----------------

def start_attendance(request):

    if not request.session.get('user'):

        return redirect('login')

    script_path = os.path.join(
        BASE_DIR,
        'phase5_recognition_with_attendance.py'
    )

    subprocess.run([
        'python',
        script_path
    ])

    messages.success(
        request,
        "Attendance Completed"
    )

    return redirect('dashboard')

# ---------------- DASHBOARD ----------------

def dashboard(request):

    if not request.session.get('user'):

        return redirect('login')

    attendance_data = []

    csv_path = os.path.join(
        BASE_DIR,
        'attendance.csv'
    )

    # ✅ READ CSV FILE

    if os.path.exists(csv_path):

        with open(
            csv_path,
            'r',
            newline='',
            encoding='utf-8'
        ) as file:

            reader = csv.reader(file)

            # SKIP HEADER
            next(reader, None)

            for row in reader:

                if len(row) >= 3:

                    attendance_data.append({

                        'name': row[0],
                        'date': row[1],
                        'time': row[2]

                    })

    return render(

        request,
        'dashboard.html',
        {
            'data': attendance_data
        }
    )

# ---------------- LOGOUT ----------------

def logout_view(request):

    request.session.flush()

    return redirect('login')