from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.template import RequestContext
from django.db.models import Q

#ALL FUNCTION BASED VIEWS

#function to verify if a user has the right to access the patient profile    
def has_patient_profile_permission(request, patient_name):
        if 'Doctor' or 'Receptionist' or 'Admin' or 'Nurse' in request.user.role:
            return True
        elif (request.user.username == patient_name):
            return True
        else:
            return False
        
#return home for each role
def return_to_home_page(request, role, patient_name):
    if role == 'Doctor':
        return redirect('usermanagement:doctor')
    if role == 'Receptionist':
        return redirect('usermanagement:receptionist')
    if role == 'Nurse':
        return redirect('usermanagement:nurse')
    if role == 'Patient':
        return redirect('usermanagement:patient_profile', role=role, patient_name=patient_name)
    
#search function
def search(request):
    patients = []
    role = request.GET.get('role')
    if role == 'Patient':
        messages.info(request, "You are not allowed to search")
        return return_to_home_page(request, role, request.user.username)
    else:
        if request.method == 'POST':
            search = request.POST.get('search')
            if search is not None:
                users = CustomUser.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
                if len(users) > 0:
                    for user in users:
                        try:
                            patients.append(Patient.objects.get(user=user))
                        except ObjectDoesNotExist:
                            pass
                    if len(patients) == 0:
                            messages.info(request, "Patient with Name '"+ search + "' does not exist")
                            return return_to_home_page(request, role, 'None')
                    else:
                        context = {
                                'patients': patients,
                                'role': role
                                }
                        return render(request, 'usermanagement/'+role.lower()+'-all-patients.html',context)
                        
                else:
                    messages.info(request, "Patient with Name '"+ search + "' does not exist")
                    return return_to_home_page(request, role, 'None')
            else:
                messages.info(request, "Please enter a keyword to search")
                return return_to_home_page(request, role, 'None')
        
        messages.info(request, "Please enter a keyword to search")
        return return_to_home_page(request, role, 'None')
            

#view logic

#the index view that appears when you first launch the application
def index(request):
    return render(request, 'usermanagement/index.html')

#the home view after sign in
@login_required
def home(request):
    context = {
        'departments': Department.objects.all()
    }
    return render(request, 'usermanagement/home.html', context)

def handler404(request, *args, **argv):
    response = render(request, 'usermanagement/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'usermanagement/500.html')
    response.status_code = 500
    return response

#the receptionist view
@login_required
def receptionist(request):
    request.user.active_role = 'Receptionist'
    request.user.save()
    
    #logic for post requests
    if request.method == 'POST':
        #get patient information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tel = request.POST.get('tel')
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
        #if not,  create a new patient
        except ObjectDoesNotExist:
            patient = Patient.objects.create(
                user = user,
                place_of_birth = place_of_birth,
                person_to_contact = person_to_contact,
                person_to_contact_tel = phone_no,
                gender = gender,
            )
            
            #add patient to the user roles
            user.add_role('Patient')
            
            #save the user attributes that have not been saved aready
            user.add_user_info(first_name, last_name, tel, address, date_of_birth, profession)
            
            #add the registration bill to the patient bill report 
            bill_book = get_object_or_404(BillBook, patient=patient)
            Bill.objects.create(bill_book=bill_book, description="RB", amount=500)
            
            messages.info(request, "Patient has been registered")
            return redirect("usermanagement:all_patients", role = "Receptionist")
        
        
    context = {
        'all_users': [user.username for user in CustomUser.objects.all()],
        'all_patients': [patient.user.username for patient in Patient.objects.all()],
        'all_doctors': [doctor.user.username for doctor in Doctor.objects.all()]
    }
    return render(request, 'usermanagement/receptionist.html',context)


#function that handles registering consultations
def consultation(request):
    if request.method == 'POST':
        #get the selected patient and doctor from the consultation form
        selected_patient = request.POST.get('selected_patient')
        selected_doctor = request.POST.get('selected_doctor')
        patient = Patient.objects.get(user=CustomUser.objects.get(username=selected_patient))
        doctor = Doctor.objects.get(user=CustomUser.objects.get(username=selected_doctor))
        #verify if the patient has an on going consultation, before creating a new one
        try:
            consultation = Consultation.objects.filter(patient=patient).last()
            if consultation.status == "Pending":
                messages.info(request, f"{patient} has a Pending consultation appointment with {consultation.doctor.user.username}")
                return redirect("usermanagement:add_consultation")
            if consultation.status == "On Hold":
                messages.info(request, f"{patient}'s consultation appointment is still On Hold")
                return redirect("usermanagement:add_consultation")
            #if the consultation is complete, create a new consultation
            if consultation.status == "Complete":
                bill_book = get_object_or_404(BillBook, patient=patient)
                if bill_book.bill_set.filter(description='CB').last() is not None:
                    if bill_book.bill_set.filter(description='CB').last().paid:
                        Consultation.objects.create(
                        patient = patient,
                        doctor = doctor,
                        status = 'Pending'
                        )
                        #add the Consultation fee to the patient bill report 
                        Bill.objects.create(bill_book=bill_book, description="CB", amount=2000)
                    else:
                        messages.info(request, "Patient has not paid their last consultation fee")
                        return redirect("usermanagement:add_consultation")
                else:
                    Consultation.objects.create(
                        patient = patient,
                        doctor = doctor,
                        status = 'Pending'
                        )
                    #add the Consultation fee to the patient bill report 
                    Bill.objects.create(bill_book=bill_book, description="CB", amount=2000)
                
        #if there isn't any on going consultation, create a new consultation
        except (ObjectDoesNotExist, IndexError, AttributeError):
            if len(patient.patientvitalcard_set.all()) < 1:
                messages.info(request, "Request patient to take vital signs")
                return redirect("usermanagement:add_consultation")
            Consultation.objects.create(
                patient = patient,
                doctor = doctor,
                status = 'Pending'
                )
            
            #add the Consultation fee to the patient bill report 
            bill_book = get_object_or_404(BillBook, patient=patient)
            Bill.objects.create(bill_book=bill_book, description="CB", amount=2000)
            
    #return to the consultation queue to see that the created consultation has been added to queue
    messages.info(request, "Consultation appointment succefully added to queue")  
    return redirect("usermanagement:consultation_queue", consultant='Receptionist')


#receptionist view for all patients
@login_required
def all_patients(request, role):
    context = {
        'patients': Patient.objects.all().order_by('-created'),
        'role': role
    }
    
    #verify if the reqeust is sent by a Receptionist and load the receptionist dashboard
    if role == 'Receptionist':
        return render(request, 'usermanagement/receptionist-all-patients.html',context)
    #verify if the request is sent by a Doctor and load the doctor's dashboard
    if role == 'Doctor':
        return render(request, 'usermanagement/doctor-all-patients.html', context)
    #verify if the request is sent by a Nurse and load the nurse's Dashboard
    if role == 'Nurse':
        return render(request, 'usermanagement/nurse-all-patients.html', context)
    #generically return the base all_patients templates 
    return render(request, 'usermanagement/all-patients.html',context)
    

#patient profile view
def patient_profile(request,role, patient_name):
    request.user.active_role = role
    request.user.save()
    
    #verify if the request has permissions to the profile page of the user and hence give access to the request
    if(has_patient_profile_permission(request, patient_name)):
        
        #then get the context data ie: patient, vitals, contultation etc
        try:
            patient = Patient.objects.get(user = CustomUser.objects.get(username = patient_name))
        except ObjectDoesNotExist:
            messages.info(request, "Patient does not exist")
            return redirect('usermanagement:home')
        
        try:
            vitals = PatientVitalCard.objects.filter(patient = patient).latest('created') 
        except ObjectDoesNotExist:
            vitals = None
        
        try:
            consultation = Consultation.objects.get(id=int(request.GET.get('conId')))
        except ObjectDoesNotExist:
            messages.info(request, "Consultation number is invalid")
            return redirect("usermanagement:doctor")
        except TypeError:
            consultation = None
        try:
            bill_book = BillBook.objects.get(patient=patient)
        except ObjectDoesNotExist:
            bill_book = None
        
        context = {
            'patient': patient,
            'vitals': vitals,
            'conId': request.GET.get('conId'),
            'consultation': consultation,
            'consultations':Consultation.objects.filter(patient=patient),
            'role': role, 
            'bill_book': bill_book
        }
        #use the role to determine read/write access to the patient profile
        if role == 'Receptionist':
            return render(request, 'usermanagement/receptionist-patient-profile.html',context)
        elif role == 'Doctor':
            if Consultation is not None:
                try:
                    Report = DoctorReport.objects.get(consultation=consultation)
                    context['observations'] = Report.observations
                    context['references'] = Report.Ref
                    context['prescriptions'] = Report.prescriptions
                    context['lab_tests'] = LabTest.objects.get(consultation=consultation).tests
                except ObjectDoesNotExist:
                    pass
            return render(request, 'usermanagement/doctor-patient-profile.html',context)
        #if the request is sent by the owner of the profile
        elif request.user.username == patient_name:
            return render(request, 'usermanagement/patient.html',context)
        elif role == 'Nurse':
            return render(request, 'usermanagement/nurse-patient-profile.html',context)
        else:
            messages.info(request, "You do not have the permissons to acces this profile page")
            return return_to_home_page(request, role, patient_name)
    
    #if the request does not have access to the patient profile, prompt the client to register to gain access
    else:
        messages.info(request, "Please register as a patient to access this interface")
        return return_to_home_page(request, role, patient_name)
    
    
#nurse functionality
@login_required
def nurse(request):
    request.user.active_role = 'Nurse'
    request.user.save()
    #get context data
    context = {
        'all_patients': Patient.objects.all(),
    }
    
    if request.method == 'POST':
        #if the post request is to register patient vitals, get patient vitals from registration form
        selected_patient = request.POST.get('selected_patient')
        temperature = request.POST.get('temperature')
        pulse = request.POST.get('pulse')
        respiration_rate = request.POST.get('respiration_rate')
        oxygen_saturation = request.POST.get('oxygen_saturation')
        blood_pressure = request.POST.get('blood_pressure')
        weight = request.POST.get('weight')
        

        try:
            #create the patient vital card
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


#consultation queue 
#the consultation queue is the list of on going consultations which is filtered with respect to the client making the request
def consultation_queue(request, consultant):
    
    #if the client is a receptionist
    if consultant == 'Receptionist':
        consultations = Consultation.objects.all()
        consultation_list = []
        for consultation in consultations:
            if consultation.status == 'Pending' or consultation.status == 'On Hold':
                consultation_list.append(consultation)
        context = {
        'consultations': consultation_list,
        'consultant': consultant
        } 
        return render(request, 'usermanagement/general-consultation-queue.html', context)
    
    #if the client is a doctor
    if consultant == 'Doctor':
        consultations = Consultation.objects.filter(doctor=Doctor.objects.get(user=request.user))
        consultation_list = []
        for consultation in consultations:
            if consultation.status == 'Pending' or consultation.status == 'On Hold':
                consultation_list.append(consultation)
        context = {
        'consultations': consultation_list,
        'consultant': consultant
        } 
        return render(request, 'usermanagement/doctor-consultation-queue.html', context)
    
    #if the client is a patient
    if consultant == 'Patient':
        #return the list of consultations that have thesame docotor in common with the patient making the request
        try:
            consultation = Consultation.objects.filter(patient=Patient.objects.get(user=request.user)).last()
        except (IndexError, ObjectDoesNotExist, AttributeError):
            consultations = None
            consultation = None
            
        consultation_list = []
        if consultation is not None:
            consultations = Consultation.objects.filter(doctor=consultation.doctor)
            for consultation in consultations:
                if consultation.status == 'Pending' or consultation.status == 'On Hold':
                    consultation_list.append(consultation)
                    
        #get the number of the next patient to be consulted in queue
        next_in_queue = None
        for consultation in consultation_list:
            if consultation.status == 'Pending':
                next_in_queue = consultation.id
                break
            
        context={
            'consultations': consultation_list,
            'consultant': consultant,
            'next_in_queue': next_in_queue
        }
        return render(request, 'usermanagement/patient-consultation-queue.html', context)

#function to obtain context data for adding a consultation
def add_consultation(request):
    context = {
        'all_users': [user.username for user in CustomUser.objects.all()],
        'all_patients': [patient.user.username for patient in Patient.objects.all()],
        'all_doctors': [doctor.user.username for doctor in Doctor.objects.all()]
    }
    return render(request, 'usermanagement/add-consultation.html',context)


#doctor report after consultation
def doctor_report(request, conId):
    
    consultation = Consultation.objects.get(id=conId)
    patient = consultation.patient
    try:
        Report = DoctorReport.objects.get(consultation = consultation)
    except ObjectDoesNotExist:
        Report = DoctorReport.objects.create(
            consultation = consultation
        )
    
    try:
        Lab_Test = LabTest.objects.get(consultation = consultation)
    except ObjectDoesNotExist:
        Lab_Test = LabTest.objects.create(
            consultation = consultation
        )

    if request.method == 'POST':
        #logic handling the submit request to each option in the doctor report view
        observations = request.POST.get('observations')
        if observations is not None:
            Report.observations = observations
            Report.save()
        ref = request.POST.get('references')
        if ref is not None:
            Report.Ref = ref
            Report.save()
        prescriptions = request.POST.get('prescriptions')
        if prescriptions is not None:
            Report.prescriptions = prescriptions
            Report.save()
        lab_tests = request.POST.get('lab_tests')
        if lab_tests is not None:
            Lab_Test.tests = lab_tests
            Lab_Test.save()
        admitted = request.POST.get('admit')
        if admitted is not None:
            if admitted == 'Yes':
                Report.admitted  = True
                Report.save()
                patient.admitted = True
                patient.save()
            if admitted == 'No':
                Report.admitted  = False
                Report.save()
                patient.admitted = False
                patient.save()
        complete_consultation = request.POST.get('complete_consultation')
        if complete_consultation is not None:
            consultation.status = 'Complete'
            consultation.save()
            return redirect('/doctor')
        hold_consultation = request.POST.get('hold_consultation')
        if hold_consultation is not None:
            consultation.status = 'On Hold'
            consultation.save()
            return redirect('/doctor')
        
    return redirect('/Doctor/profile/'+consultation.patient.user.username+'/?conId='+str(consultation.id))


#consultation info view
def consultation_info(request, conId):
    consultation = get_object_or_404(Consultation, pk=conId)
    report = get_object_or_404(DoctorReport, consultation=consultation)
    lab_tests = get_object_or_404(LabTest, consultation=consultation)
    #get the consultation doctor so he can make modifications to the consultation
    context = {
        'consultation': consultation,
        'patient': consultation.patient,
        'report': report,
        'lab_tests': lab_tests,
        'conId': consultation.id
        }
    return render(request, 'usermanagement/consultation-info.html', context)


#modify prescription
def modify_prescription(request, conId):
    consultation = Consultation.objects.get(id=conId)
    try:
        Report = DoctorReport.objects.get(consultation = consultation)
    except ObjectDoesNotExist:
        messages.info(request, "No such Report")
        return return_to_home_page(request, 'Doctor', 'None')
    
    prescriptions = request.POST.get('prescriptions')
    if prescriptions is not None:
        Report.prescriptions = prescriptions
        Report.save() 
    return redirect('usermanagement:consultation_info', conId=consultation.id)


#doctor functionality
@login_required
def doctor(request):
    request.user.active_role = 'Doctor'
    request.user.save()
    return redirect('usermanagement:consultation_queue', consultant = 'Doctor')

@login_required
def payment(request):
    bill_book = None
    if request.method == 'POST':
        selected_patient = request.POST.get('selected_patient')
        patient = Patient.objects.get(user=CustomUser.objects.get(username=selected_patient))
        bill_book = get_object_or_404(BillBook, patient=patient)
        
    context = {
        'all_patients': [patient.user.username for patient in Patient.objects.all()],
        'bill_book': bill_book
    }
    return render(request, 'usermanagement/payment.html', context)

@login_required
def paybill(request, id):
    bill = Bill.objects.get(id=id)
    bill.paid = True
    bill.save()
    messages.info(request, "Payment succesfull")
    return redirect('usermanagement:payment')


@login_required
def patient(request):
    request.user.active_role = 'Patient'
    return render(request, 'usermanagement/patient.html')

def department_info(request, id):
    pass

# ALL CLASS BASED VIEWS

#consultation delete view
class ConsultationDeleteView(DeleteView):
    model = Consultation
    success_url = reverse_lazy('usermanagement:consultation_queue', kwargs = {'consultant': 'Receptionist'})

    


    
    
    
    
    
    
    
    
