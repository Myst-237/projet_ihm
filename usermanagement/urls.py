from django.urls import path, include
from .views import *
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
    path('consultation_queue/<consultant>/', consultation_queue, name="consultation_queue"),
    path('delete_consultation/<int:pk>/', ConsultationDeleteView.as_view(), name="consultation_delete"),
    path('add_consultation', add_consultation, name="add_consultation"),
    path('doctor_report/<int:conId>/' , doctor_report, name="doctor_report"),
    path('consultation_info/<int:conId>/', consultation_info, name='consultation_info'),
    path('modify_prescription/<int:conId>/',modify_prescription, name='modify_prescription')
]