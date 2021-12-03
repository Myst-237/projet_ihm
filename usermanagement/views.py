from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, Receptionist, Patient, Doctor, PatientVitalCard, Consultation

#view functions

#function to verify if a user has the write to access the patient profile    
def has_patient_profile_permission(request, patient_name):
        if 'Doctor' or 'Receptionist' or 'Admin' in request.user.role:
            return True
        elif (request.user.username == patient_name):
            return True
        else:
            return False

#view logic

#the index view that appears when you first launch the application
def index(request):
    return render(request, 'usermanagement/index.html')

#the home view after sign in
@login_required
def home(request):
    return render(request, 'usermanagement/home.html')

#the receptionist view
@login_required
def receptionist(request):
    
    #logic for post requests
    if request.method == 'POST':
        #get patient information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tel = request.POST.get('tel')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        person_to_contact = request.POST.get('person_to_contact')
        phone_no = request.POST.get('phone_no')
        selected_user = request.POST.get('selected_user')
        gender = request.POST.get('gender')
        place_of_birth = request.POST.get('place_of_birth')
        address = request.POST.get('address')
        profession = request.POST.get('profession')
        
        #get the user object for the selected user
        try:
            user = CustomUser.objects.get(username = selected_user)
        except ObjectDoesNotExist:
            messages.info(request, "User does not exist")
            return redirect("usermanagement:receptionist")
        
        #verify if the patient is already registered
        try:
            patient = Patient.objects.get(user = user)
            messages.info(request, "This patient already exists")
            return redirect("usermanagement:receptionist")
        except ObjectDoesNotExist:
            Patient.objects.create(
                user = user,
                place_of_birth = place_of_birth,
                person_to_contact = person_to_contact,
                person_to_contact_tel = phone_no,
                age = age,
                gender = gender,
            )
            
            #add patient to the user roles
            user.add_role('Patient')
            
            #save the user attributes that have not been saved aready
            user.add_user_info(first_name, last_name, tel, address, date_of_birth, profession)
            
            messages.info(request, "Patient has been registered")
            return redirect("usermanagement:all_patients", role = "Receptionist")
        
        
    context = {
        'all_users': [user.username for user in CustomUser.objects.all()],
        'all_patients': [patient.user.username for patient in Patient.objects.all()],
        'all_doctors': [doctor.user.username for doctor in Doctor.objects.all()]
    }
    return render(request, 'usermanagement/receptionist.html',context)

#consultation view 
def consultation(request):
    if request.method == 'POST':
        selected_patient = request.POST.get('selected_patient')
        selected_doctor = request.POST.get('selected_doctor')
        patient = Patient.objects.get(user=CustomUser.objects.get(username=selected_patient))
        doctor = Doctor.objects.get(user=CustomUser.objects.get(username=selected_doctor))
        try:
            consultation = Consultation.objects.get(patient=patient)
            if consultation.status == "Pending":
                messages.info(request, f"{patient} has a Pending consultation appointment with {consultation.doctor.user.username}")
                return redirect("usermanagement:receptionist")
            if consultation.status == "On Hold":
                messages.info(request, f"{patient}'s consultation appointment is still On Hold")
                return redirect("usermanagement:receptionist")
            if consultation.status == "Finished":
                Consultation.objects.create(
                patient = patient,
                doctor = doctor,
                status = 'Pending'
                )
        except ObjectDoesNotExist:
            Consultation.objects.create(
                patient = patient,
                doctor = doctor,
                status = 'Pending'
                )
    messages.info(request, "Consultation appointment succefully added to queue")  
    return redirect("usermanagement:receptionist")


#receptionist view for searching all patients
@login_required
def all_patients(request, role):
    context = {
        'patients': Patient.objects.all().order_by('-created')
    }
    
    #verify if the reqeust is sent by a Receptionist and load the receptionist dashboard
    if role == 'Receptionist':
        return render(request, 'usermanagement/receptionist-all-patients.html',context)
    return render(request, 'usermanagement/all-patients.html',context)
    

#patient profile view
def patient_profile(request,role, patient_name):
    
    #verify if the request has permissions to the profile page of the user and hence give access to the request
    if(has_patient_profile_permission(request, patient_name)):
        try:
            patient = Patient.objects.get(user = CustomUser.objects.get(username = patient_name))
        except ObjectDoesNotExist:
            messages.info(request, "Patient does not exist")
            return redirect('/home')
        try:
            vitals = PatientVitalCard.objects.filter(patient = patient).latest('created') 
        except ObjectDoesNotExist:
            vitals = None
        context = {
            'patient': patient,
            'vitals': vitals
        }
        if role == 'Receptionist':
            return render(request, 'usermanagement/receptionist-patient-profile.html',context)
        elif request.user.username == patient_name:
            return render(request, 'usermanagement/patient.html',context)
        else:
            messages.info(request, "You do not have the permissons to acces this profile page")
            return redirect('/home')

    else:
        messages.info(request, "Please register as a patient to access this interface")
        return redirect('/home')
    
#nurse functionality
@login_required
def nurse(request):
    context = {
        'all_patients': Patient.objects.all(),
    }
    
    if request.method == 'POST':
        selected_patient = request.POST.get('selected_patient')
        temperature = request.POST.get('temperature')
        pulse = request.POST.get('pulse')
        respiration_rate = request.POST.get('respiration_rate')
        oxygen_saturation = request.POST.get('oxygen_saturation')
        blood_pressure = request.POST.get('blood_pressure')
        weight = request.POST.get('weight')
        
        try:
            patient = Patient.objects.get(user = CustomUser.objects.get(username = selected_patient))
            PatientVitalCard.objects.create(
            patient = patient,
            temperature = temperature,
            pulse = pulse,
            respiration_rate = respiration_rate,
            blood_pressure = blood_pressure,
            oxygen_saturation = oxygen_saturation,
            weight = weight,
            )
            messages.info(request, "Patient vital card succefully created")
            return redirect('/nurse')
        except ObjectDoesNotExist:
            messages.info(request, "This patient does not exist")
            return redirect('/nurse')
        
    return render(request, 'usermanagement/nurse.html', context)
    
#doctor functionality
@login_required
def doctor(request):
        return render(request, 'usermanagement/doctor.html')
    
#functionality for booking appointments
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
    


    
    
    
    
    
    
    
    
