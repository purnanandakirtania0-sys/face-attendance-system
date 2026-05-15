from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    # register_date = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=200)
    
def __str__(self):
    return self.name

class Attendance(models.Model):
    student_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
def __str__(self):
    return self.student_namec    