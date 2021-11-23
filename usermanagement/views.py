from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Receptionist, Patient, Doctor
# Create your views here.

def index(request):
    return render(request, 'usermanagement/index.html')

@login_required
def home(request):
    roles = request.user.role
    print(roles)
    context = {
        'roles': roles
    }
    return render(request, 'usermanagement/home.html',context)

@login_required
def receptionist(request):
        return render(request, 'usermanagement/receptionist.html')
    

@login_required
def receptionist_all_patients(request):
    return render(request, 'usermanagement/receptionist-all-patients.html')

@login_required
def book_appointment(request):
    return render(request, 'usermanagement/book-appointment.html')

@login_required
def modify_appointment(request):
    return render(request, 'usermanagement/modify-appointment.html')

@login_required
def add_payment(request):
    return render(request, 'usermanagement/add-payment.html')

@login_required
def modify_payment(request):
    return render(request, 'usermanagement/modify-payment.html')

@login_required
def payments(request):
    return render(request, 'usermanagement/payments.html')
    
@login_required
def patient(request):
        return render(request, 'usermanagement/patient.html')
    
@login_required
def doctor(request):
        return render(request, 'usermanagement/doctor.html')
    
@login_required
def nurse(request):
        return render(request, 'usermanagement/nurse.html')
    
    