from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_page, name='login'),

    path('register-face/', views.register_face, name='register_face'),

    path('train-page/', views.train_page, name='train_page'),

    path('train-model/', views.train_model, name='train_model'),

    path('attendance-page/', views.attendance_page, name='attendance_page'),

    path('start-attendance/', views.start_attendance, name='start_attendance'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.logout_view, name='logout'),

    path('home/', views.home, name='home'),

]