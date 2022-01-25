from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta

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

Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

Status = [
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
    ('On Hold', 'On Hold'),
]

BillDescription = [
    ('CB', 'Consultaiton Bill'),
    ('RB', 'Registration Bill'),
    ('PB', 'Pharmacy Bill'),
    ('LB', 'Laboratory Bill')
]
#the custom user model that extends the django base user model adding the required attributes
class CustomUser(AbstractUser):
    role = ArrayField(models.CharField(max_length = 50, choices = Roles), default = list, null=True, blank= True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=250, blank = True, null = True)
    date_of_birth = models.DateField(blank = True, null = True)
    profession = models.CharField(max_length=100, blank = True, null = True)
    profile_pic = models.ImageField(blank = True, null = True)
    active_role = models.CharField(max_length=50, blank = True, null = True)
    
    
    def __str__(self):
        return self.username 
    
    #add a role to a user
    def add_role(self, role):
        if role in self.role:
            pass
        else:
            self.role.append(role)
            self.save()
    
    def get_age(self):
        relativeage = relativedelta(timezone.now().date(), self.date_of_birth)
        return relativeage.years
            
    #add patient/user information       
    def add_user_info(self, first_name, last_name, tel, address, date_of_birth, profession):
        self.first_name = first_name
        self.last_name = last_name
        self.tel = tel
        self.address = address
        self.date_of_birth = date_of_birth
        self.profession = profession
        self.save()
    
 
 #patient model   
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    place_of_birth = models.CharField(max_length=200)
    person_to_contact = models.CharField(max_length=100)
    person_to_contact_tel = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices = Gender)
    admitted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        
        if 'Patient' in self.user.role:
            pass
        else:
            self.user.role.append('Patient')
            self.user.save() 
            
        return super(Patient, self).save(*args, **kwargs)

        
    def delete(self, *args, **kwargs):
        if 'Patient' in self.user.role:
            self.user.role.remove('Patient')
            self.user.save()
        super(Patient, self).delete()
        
    
 #doctor model   
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    specialist = models.BooleanField(default=False)
    speciality =  models.CharField(max_length=100, default='NoSpeciality', choices = Speciality)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if 'Doctor' in self.user.role:
            pass
        else:
            self.user.role.append('Doctor')
            self.user.save()
        return super(Doctor, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if 'Doctor' in self.user.role:
            self.user.role.remove('Doctor')
            self.user.save()
        super(Doctor, self).delete()


#lab technician model
class LabTech(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.user.username

#Consultation queue
class Consultation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices = Status)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Consultation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.user.username} / {self.patient.user.username} consultation"
        
#labtest model
class LabTest(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete = models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    tests = models.TextField(null=True, blank=True)
    results = models.TextField(null=True, blank= True)
    remarks = models.TextField(null=True, blank= True)
    
    def __str__(self):
        return f"{self.consultation.patient.user.username}'s Lab test"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(LabTest, self).save(*args, **kwargs)

#doctor report after patient consultation    
class DoctorReport(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    observations = models.TextField(blank=True, null=True)
    Ref = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank = True, null = True)
    admitted = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(DoctorReport, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.consultation.patient.user.username}'s Report by {self.consultation.doctor.user.username}"    
    
    
#patient vital signs before consultation    
class PatientVitalCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    temperature = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100, blank = True, null = True)
    respiration_rate = models.CharField(max_length=100, blank = True, null = True)
    blood_pressure = models.CharField(max_length=100)
    oxygen_saturation = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(PatientVitalCard, self).save(*args, **kwargs)

    def __str__(self):
        return f"Vitals for {self.patient.user.username} <{self.created}> "
    
    
#Receptionist for patient Registration 
class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        if 'Receptionist' in self.user.role:
            pass
        else:
            self.user.role.append('Receptionist')
            self.user.save()
        return super(Receptionist, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if 'Receptionist' in self.user.role:
            self.user.role.remove('Receptionist')
            self.user.save()
        super(Receptionist, self).delete()
    

#Nurse: taking vital signs, etc.
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    def save(self, *args, **kwargs):
        if 'Nurse' in self.user.role:
            pass
        else:
            self.user.role.append('Nurse')
            self.user.save()
        return super(Nurse, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if 'Nurse' in self.user.role:
            self.user.role.remove('Nurse')
            self.user.save()
        super(Nurse, self).delete()
    
    def __str__(self):
        return f"{self.user.username}"
    
#bill book
class BillBook(models.Model):
    patient = models.OneToOneField(Patient, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BillBook, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Biil Book for {self.patient.user.username}"
    
    def get_total(self):
        total = 0
        for bill in self.bill_set.all():
            total += bill.amount
        return total

    def get_paid_total(self):
        total = 0
        for bill in self.bill_set.all():
            if bill.paid:
                total += bill.amount
        return total
    
    def get_unpaid_total(self):
        total = 0
        for bill in self.bill_set.all():
            if not bill.paid:
                total += bill.amount
        return total
    
#bill
class Bill(models.Model):
    bill_book = models.ForeignKey(BillBook, on_delete = models.CASCADE)
    description = models.CharField(max_length=50, choices=BillDescription)
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Bill, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Biil for {self.bill_book.patient.user.username}"
    
    

#HOOKS
@receiver(pre_delete, sender=Patient)
def delete_patient_role_hook(sender, instance, using, **kwargs): 
    if 'Patient' in instance.user.role:
            instance.user.role.remove('Patient')
            instance.user.save()  

@receiver(pre_delete, sender=Doctor)
def delete_doctor_role_hook(sender, instance, using, **kwargs): 
    if 'Doctor' in instance.user.role:
            instance.user.role.remove('Doctor')
            instance.user.save()  
            
@receiver(pre_delete, sender=Receptionist)
def delete_receptionist_role_hook(sender, instance, using, **kwargs): 
    if 'Receptionist' in instance.user.role:
            instance.user.role.remove('Receptionist')
            instance.user.save()  
            
@receiver(pre_delete, sender=Nurse)
def delete_nurse_role_hook(sender, instance, using, **kwargs): 
    if 'Nurse' in instance.user.role:
            instance.user.role.remove('Nurse')
            instance.user.save()  

@receiver(pre_delete, sender=Consultation)
def delete_consultation_bill_hook(sender, instance, using, **kwargs):
    try:
        bill_book = BillBook.objects.get(patient=instance.patient)
        bill_book.bill_set.all().last().delete()
    except ObjectDoesNotExist:
        pass
    
    
@receiver(post_save, sender=Patient)
def add_registration_bill_hook(sender, instance, **kwargs):
    try: 
        bill_book = BillBook.objects.get(patient=instance)
    except (ObjectDoesNotExist, ValueError):
        BillBook.objects.create(patient=instance)
