from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, PatientForm, AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment
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