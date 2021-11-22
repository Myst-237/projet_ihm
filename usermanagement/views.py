from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
Roles = [
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
    ('Receptionist', 'Receptionist'),
    ('Admin', 'Admin'),
    ('Accountant', 'Accountant'),
    ('Nurse', 'Nurse'),
    ('Labtech', 'Labtech'),
    ('HRM', 'HRM'),
    ('Specialist', 'Specialist'),
]

def index(request):
    return render(request, 'usermanagement/index.html')

@login_required
def home(request):
    role_list = []
    for object1,object2 in Roles:
        role_list.append(object1)
    
    context = {
        'role_list' : role_list,
    }
    return render(request, 'usermanagement/home.html',context)