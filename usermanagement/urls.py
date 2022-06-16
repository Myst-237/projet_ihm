from django.urls import path, include
from .views import *
app_name = 'usermanagement'

urlpatterns = [
    path('', index , name="index"),
    path('administrator/', administrator, name="administrator"),
    path('administrator/add-doctor', DoctorCreateView.as_view(), name="add-doctor"),
    path('administrator/list-doctors', DoctorListView.as_view(), name="list-doctors"),
    path('administrator/delete-doctor/<int:pk>/', DoctorDeleteView.as_view(), name="delete-doctor"),
    path('administrator/add-receptionist', ReceptionistCreateView.as_view(), name="add-receptionist"),
    path('administrator/list-receptionists', ReceptionistListView.as_view(), name="list-receptionists"),
    path('administrator/delete-receptionist/<int:pk>/', ReceptionistDeleteView.as_view(), name="delete-receptionist"),
    path('administrator/add-nurse', NurseCreateView.as_view(), name="add-nurse"),
    path('administrator/list-nurses', NurseListView.as_view(), name="list-nurses"),
    path('administrator/delete-nurse/<int:pk>/', NurseDeleteView.as_view(), name="delete-nurse"),
    path('administrator/list-patients', PatientListView.as_view(), name="list-patients"),
    path('administrator/delete-patient/<int:pk>/',PatientDeleteView.as_view(), name="delete-patient"),
    path('<int:pk>/user-profile/', UserUpdateView.as_view(), name="user-profile"),
    path('home/', home , name="home"),
    path('receptionist/', receptionist_home , name="receptionist_home"),
    path('receptionist/add_patient', receptionist , name="receptionist"),
    path('<role>/all_patients/', all_patients , name="all_patients"),
    path('receptionist/payment', payment, name="payment"),
    path('receptionist/paybill/<int:id>/', paybill, name="paybill"),
    path('receptionist/consultation', consultation, name="consultation"),
    path('<role>/profile/<patient_name>/', patient_profile, name="patient_profile"),
    path('nurse/', nurse_home , name="nurse_home"),
    path('nurse/takevitals', nurse , name="nurse"),
    path('doctor/', doctor , name="doctor"),
    path('consultation_queue/<consultant>/', consultation_queue, name="consultation_queue"),
    path('delete_consultation/<int:pk>/', ConsultationDeleteView.as_view(), name="consultation_delete"),
    path('add_consultation', add_consultation, name="add_consultation"),
    path('doctor_report/<int:conId>/' , doctor_report, name="doctor_report"),
    path('consultation_info/<int:conId>/', consultation_info, name='consultation_info'),
    path('modify_prescription/<int:conId>/',modify_prescription, name='modify_prescription'),
    path('search/', search , name="search"),
    path('department_info/<int:id>/', department_info, name='department_info')
]