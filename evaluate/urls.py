from django.urls import path
from wizard.api.views import *
from .views import *
app_name = "wizard-api"

urlpatterns = [
    path('ProjectsApiView/', ProjectsApiView.as_view(), name='ProjectsApiView'),
    path('AddPeriodApiView/', AddPeriodApiView.as_view(), name='AddPeriodApiView'),
    path('AddFrequencyApiView/', AddFrequencyApiView.as_view(), name='AddFrequencyApiView'),
    path('Frequencies/', Frequencies.as_view(), name='Frequencies'),
    path('employee/<int:id>',EmployeeListForScores.as_view(),name='employee'),
    path('EvaluationList/',EvaluationList.as_view(),name='EvaluationList'),
    path('PerformCardUpdateView/',PerformCardUpdateView.as_view(),name='PerformCardUpdateView'),
    path('EvaluateComptencyList/<int:id>',EvaluateComptencyList.as_view(),name='EvaluateComptencyList'),
    path('EmployeePerformance/',EmployeePerformance.as_view(),name='EmployeePerformance'),#son sehife
    path('FreqSetActive/',FreqSetActive.as_view(),name='FreqSetActive'),
]