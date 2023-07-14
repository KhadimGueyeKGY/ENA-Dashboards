from django.shortcuts import render
 
from ENA_Datahub_Dashboard.ENADatahubDashboard import app as dash_app


def dash_view(request):
        return render(request, 'ena_datahub_dashboard.html')
