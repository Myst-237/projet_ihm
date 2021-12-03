from django.urls import path, include
from .views import (index,home,receptionist,all_patients,book_appointment,add_payment,modify_appointment,
                    modify_payment,payments,patient_profile,doctor,nurse,consultation)

app_name = 'usermanagement'

urlpatterns = [
    path('', index , name="index"),
    path('home/', home , name="home"),
    path('receptionist/', receptionist , name="receptionist"),
    path('<role>/all_patients/', all_patients , name="all_patients"),
    path('receptionist/book_appointment/', book_appointment , name="book_appointment"),
    path('receptionist/modify_appointment/', modify_appointment, name="modify_appointment"),
    path('receptionist/add_payment', add_payment, name="add_payment"),
    path('receptionist/modify_payment', modify_payment, name="modify_payment"),
    path('receptionist/payments', payments, name="payments"),
    path('receptionist/consultation', consultation, name="consultation"),
    path('<role>/profile/<patient_name>/', patient_profile, name="patient_profile"),
    path('nurse/', nurse , name="nurse"),
    path('doctor/', doctor , name="doctor"),
]