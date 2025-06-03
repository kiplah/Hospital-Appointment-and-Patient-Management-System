from django.contrib.auth.models import User
from django.db import models

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.user.username} - {self.appointment_date}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"History for {self.patient.user.username}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

