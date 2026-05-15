from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home'),

    path('login/', views.login_page, name='login'),

    path('attendance-page/', views.attendance_page, name='attendance_page'),

    path('train-page/', views.train_page, name='train_page'),

    path('dashboard-page/', views.dashboard_page, name='dashboard_page'),

    path('register-face/', views.register_face, name='register_face'),

]