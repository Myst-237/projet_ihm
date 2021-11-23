from django.urls import path, include
from .views import (index,home,receptionist,receptionist_all_patients,book_appointment,add_payment,modify_appointment,
                    modify_payment,payments,patient,doctor,nurse)

app_name = 'usermanagement'

urlpatterns = [
    path('', index , name="index"),
    path('home/', home , name="home"),
    path('receptionist/', receptionist , name="receptionist"),
    path('doctor/', doctor , name="doctor"),
    path('patient/', patient , name="patient"),
    path('nurse/', nurse , name="nurse"),
    path('receptionist/all_patients/', receptionist_all_patients , name="receptionist_all_patients"),
    path('receptionist/book_appointment/', book_appointment , name="book_appointment"),
    path('receptionist/modify_appointment/', modify_appointment, name="modify_appointment"),
    path('receptionist/add_payment', add_payment, name="add_payment"),
    path('receptionist/modify_payment', modify_payment, name="modify_payment"),
    path('receptionist/payments', payments, name="payments")
]