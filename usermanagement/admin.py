from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']
    readonly_fields = ['role']
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Profile',
            {
                'fields':(
                    'role',
                    'tel', 
                    'address',
                    'date_of_birth',
                    'profession', 
                    'profile_pic',
                    'active_role',
                    'about'
                )
            }
        )
    )

class PatientAdmin(admin.ModelAdmin):
   readonly_fields = ['admitted', 'created', 'modified']
   
class PatientVitalCardAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']

class DoctorReportAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']

class LabTestAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']

class ConsultationAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Receptionist)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor)
admin.site.register(PatientVitalCard, PatientVitalCardAdmin)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(DoctorReport, DoctorReportAdmin)
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(Nurse)
admin.site.register(BillBook)
admin.site.register(Bill)
admin.site.register(Department)