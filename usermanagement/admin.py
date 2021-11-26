from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Receptionist,Patient,Doctor, PatientVitalCard

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']
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
                    'profile_pic'
                )
            }
        )
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Receptionist)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientVitalCard)