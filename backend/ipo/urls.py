from django.urls import path
from . import views

app_name = 'ipo'

urlpatterns = [
    path('', views.ipo_dashboard, name='dashboard'),
] 