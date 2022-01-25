from django.urls import path, include
from .views import *
app_name = 'usermanagement'

urlpatterns = [
    path('', index , name="index"),
    path('home/', home , name="home"),
    path('receptionist/', receptionist , name="receptionist"),
    path('<role>/all_patients/', all_patients , name="all_patients"),
    path('receptionist/payment', payment, name="payment"),
    path('receptionist/paybill/<int:id>/', paybill, name="paybill"),
    path('receptionist/consultation', consultation, name="consultation"),
    path('<role>/profile/<patient_name>/', patient_profile, name="patient_profile"),
    path('nurse/', nurse , name="nurse"),
    path('doctor/', doctor , name="doctor"),
    path('consultation_queue/<consultant>/', consultation_queue, name="consultation_queue"),
    path('delete_consultation/<int:pk>/', ConsultationDeleteView.as_view(), name="consultation_delete"),
    path('add_consultation', add_consultation, name="add_consultation"),
    path('doctor_report/<int:conId>/' , doctor_report, name="doctor_report"),
    path('consultation_info/<int:conId>/', consultation_info, name='consultation_info'),
    path('modify_prescription/<int:conId>/',modify_prescription, name='modify_prescription'),
    path('search/', search , name="search"),
]