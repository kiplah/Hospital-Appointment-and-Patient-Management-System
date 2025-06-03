from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # 👈 default route
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/', views.view_appointments, name='view_appointments'),
]
