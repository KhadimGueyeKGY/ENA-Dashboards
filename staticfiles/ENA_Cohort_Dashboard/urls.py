from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dash_view, name='ena-cohort-dashboard'),
    #path('ena-cohort-dashboard/', views.dash_view, name='ena-cohort-dashboard')
]
