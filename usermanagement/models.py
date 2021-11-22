from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

#importing the user model from settings
User = settings.AUTH_USER_MODEL

#creating the different roles in the hospital
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

#creating the different specialities for specialist doctors
Speciality = [
    ('NoSpeciality', 'NoSpeciality'),
    ('Dermatology', 'Dermatology'),
    ('Radiology', 'Radiology'),
]

#the custom user model that extends the django base user model adding the required attributes
class CustomUser(AbstractUser):
    role = ArrayField(models.CharField(max_length = 50, choices = Roles), default = list)
    tel = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=250, blank = True, null = True)
    date_of_birth = models.DateField(blank = True, null = True)
    profession = models.CharField(max_length=100, blank = True, null = True)
    profile_pic = models.ImageField(blank = True, null = True)
    
    
    def __str__(self):
        return self.username 
    
 
 #patient model   
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    place_of_birth = models.CharField(max_length=200)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_tel = models.CharField(max_length=100)
    person_to_contact = models.CharField(max_length=100)
    person_to_contact_tel = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
    
 #doctor model   
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    specialist = models.BooleanField(default=False)
    speciality =  models.CharField(max_length=100, default='NoSpeciality', choices = Speciality)
    
    def __str__(self):
        return self.user.username


#lab technician model
class LabTech(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.user.username
        
#labtest model
class LabTest(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete= models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    created = models.DateField()
    modified = models.DateField()
    tests = models.TextField()
    results = models.TextField()
    remarks = models.TextField()
    
    def __str__(self):
        return f"{self.patient.username}'s Lab test"
    

#doctor report after patient consultation    
class DoctorReport(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank = True, null = True)
    lab_tests = models.ForeignKey(LabTest, on_delete = models.CASCADE)
    admitted = models.BooleanField(default = False)
    remarks = models.TextField(blank = True, null = True)
    created = models.DateField()
    modified = models.DateField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient.username}'s Report by {self.doctor.username}"    
    
    
#patient vital signs before consultation    
class PatientVitalCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    temperature = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100)
    respiration_rate = models.CharField(max_length=100)
    blood_pressure = models.CharField(max_length=100)
    oxygen_saturation = models.CharField(max_length=200)
    wieght = models.CharField(max_length=100)
    created = models.DateField()
    modified = models.DateField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"Vitals for {self.patient.username}"
    
    
#Receptionist for patient Registration 
class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    

#Nurse: taking vital signs, etc.
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    
    
    
    
    
    
    