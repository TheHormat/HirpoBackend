from django.urls import path
from wizard.api.views import *

app_name = "wizard-api2"

urlpatterns = [
    path("employees/", UserListView.as_view(), name="employees"),
    
    path("start", CreateProjectView.as_view(), name="start"),
    path("CreateProject/", CreateProjectWithoutWizardView.as_view(), name="CreateProjectWithoutWizardView"),
    path("CreatePositionView/", CreatePositionView.as_view(), name="CreatePositionView"),
    
    path("positionupdate", PositionUpdateView.as_view(), name="positionupdate"),
    
    path("ListPositionView/", ListPositionView.as_view(), name="ListPositionView"),
    path("depposition/", DepartmentPositionListView.as_view(), name="depposition"),
    path("goback", go_back.as_view(), name="go_back"),
    path('upload/', ExcellUploadView.as_view(), name='upload_excel'),
    path('download', OneTimeView.as_view(), name='download_excel'),
    path("DepartmentUpdate/", DepartmentUpdateView.as_view(), name="DepartmentUpdate"),
    path("WizardComptencySaveView", WizardComptencySaveView.as_view(), name="WizardComptencySaveView"),
    path("weightUpdateView", WeightUpdateView.as_view(), name="WeightUpdateView"),
    path("project_delete", project_delete.as_view(), name="project_delete"),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('DpForChart/', DepartmentForOrganizitialChart.as_view(), name='DepartmentForOrganizitialChart'),
    path('EmployeeSingle/<id>', EmployeeSingleView.as_view(), name='EmployeeSingleView'),
    path('EmployeePageView/', EmployeePageView.as_view(), name='EmployeePageView'),
    
    path('EmployeeListView/', EmployeeListView.as_view(), name='EmployeeListView'),
    path('AddUser/', AddUser.as_view(), name='AddUser'),
    path('PositionSelect/', PositionSelect.as_view(), name='PositionSelect'),
    path('UserChange/<id>', UserChange.as_view(), name='UserChange'),
    path('ChangePPView/', ChangePPView.as_view(), name='ChangePPView'),
    path('HomePageView/', HomePageView.as_view(), name='HomePageView'),
    path('AddjsonView/', AddjsonView.as_view(), name='AddjsonView'),
    path('Get_Weights/', Get_Weights.as_view(), name='Get_Weights'),
    path('CreateMainSkill/', CreateMainSkill.as_view(), name='CreateMainSkill'),
    path('PositionAddView/', PositionAddView.as_view(), name='PositionAddView'),
    path('CheckUserPermission/', CheckUserPermission.as_view(), name='CheckUserPermission'),
    path('MakeVisibledScore/', MakeVisibledScore.as_view(), name='MakeVisibledScore'),
    path('PositionDeleteView/<id>/', PositionDeleteView.as_view(), name='PositionDeleteView'),

]