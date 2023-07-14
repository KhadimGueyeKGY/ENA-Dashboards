from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dash_view, name='ena-datahub-dashboard'),
    #path('ena-datahub-dashboard/', views.dash_view, name='ena-datahub-dashboard')
]
