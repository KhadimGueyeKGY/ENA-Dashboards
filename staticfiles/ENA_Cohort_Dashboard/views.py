from django.shortcuts import render
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.main import app as dash_app2
  
#from Home.main import app as dash_app


def dash_view(request):
        return render(request, 'ENA_Cohort_Dashboard.html')
