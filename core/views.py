from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, PatientForm, AppointmentForm, MedicalHistoryForm, DoctorRegistrationForm, DoctorProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Appointment, Patient, MedicalHistory, Doctor
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.db.models import Q

def home(request):
    return render(request, 'core/home.html', {'now': now()})

def choose_role(request):
    return render(request, 'core/choose_role.html')

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
def register_doctor(request):
    if request.method == 'POST':
        user_form = DoctorRegistrationForm(request.POST)
        profile_form = DoctorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            doctor = profile_form.save(commit=False)
            doctor.user = user
            doctor.save()
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        user_form = DoctorRegistrationForm()
        profile_form = DoctorProfileForm()
    return render(request, 'core/register_doctor.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query)
        )
    else:
        patients = Patient.objects.all()

    return render(request, 'core/doctor_dashboard.html', {
        'patients': patients,
        'now': now(),
        'query': query or ''
    })
@user_passes_test(is_doctor)
def edit_medical_history(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical history updated.")
            return redirect('view_medical_history', patient_id=history.patient.id)
    else:
        form = MedicalHistoryForm(instance=history)
    return render(request, 'core/edit_medical_history.html', {
        'form': form,
        'patient': history.patient
    })
@user_passes_test(is_doctor)
def delete_medical_history(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)
    patient_id = history.patient.id
    history.delete()
    messages.success(request, "Medical history entry deleted.")
    return redirect('view_medical_history', patient_id=patient_id)
@login_required
def dashboard(request):
    user = request.user

    if hasattr(user, 'patient'):
        appointments = Appointment.objects.filter(patient=user.patient).order_by('appointment_date')
        doctors = Doctor.objects.select_related('user').all()
        return render(request, 'core/dashboard.html', {
            'appointments': appointments,
            'doctors': doctors,
            'user': user
        })

    elif hasattr(user, 'doctor'):
        return redirect('doctor_dashboard')

    else:
        return HttpResponseForbidden("You do not have access to this dashboard.")




@login_required
def book_appointment(request):
    patient = request.user.patient
    doctor_id = request.GET.get('doctor')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect('dashboard')
    else:
        form = AppointmentForm(initial={'doctor': doctor_id} if doctor_id else None)

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

    if hasattr(request.user, 'patient') and request.user.patient.id != patient.id:
        return HttpResponseForbidden("Access denied.")

    histories = MedicalHistory.objects.filter(patient=patient).order_by('-updated_at')
    return render(request, 'core/view_medical_history.html', {
        'patient': patient,
        'histories': histories
    })
