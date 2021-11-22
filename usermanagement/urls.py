from django.urls import path, include
from .views import index,home

app_name = 'usermanagement'

urlpatterns = [
    path('', index , name="index"),
    path('home/', home , name="home"),
]