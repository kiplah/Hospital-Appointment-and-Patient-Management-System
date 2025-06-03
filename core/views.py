from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, PatientForm, AppointmentForm, MedicalHistoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Appointment, Patient, MedicalHistory
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        patient_form = PatientForm()
    return render(request, 'core/register.html', {'user_form': user_form, 'patient_form': patient_form})
def is_doctor(user):
    return hasattr(user, 'doctor')

@user_passes_test(is_doctor)
def add_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            history.save()
            return redirect('view_medical_history', patient_id=patient.id)
    else:
        form = MedicalHistoryForm()
    return render(request, 'core/add_medical_history.html', {'form': form, 'patient': patient})

@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'core/dashboard.html', {'appointments': appointments})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    appointment.delete()
    messages.success(request, "Appointment cancelled.")
    return redirect('dashboard')
@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient).order_by('appointment_date')
    return render(request, 'core/view_appointments.html', {'appointments': appointments})
@login_required
def view_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    histories = MedicalHistory.objects.filter(patient=patient).order_by('-updated_at')
    return render(request, 'core/view_medical_history.html', {'patient': patient, 'histories': histories})
