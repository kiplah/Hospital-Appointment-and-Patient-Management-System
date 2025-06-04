from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.choose_role, name='choose_role'),
    path('register/patient/', views.register, name='register'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('history/<int:patient_id>/', views.view_medical_history, name='view_medical_history'),
    path('history/add/<int:patient_id>/', views.add_medical_history, name='add_medical_history'),
    path('history/edit/<int:history_id>/', views.edit_medical_history, name='edit_medical_history'),
    path('history/delete/<int:history_id>/', views.delete_medical_history, name='delete_medical_history'),

]
