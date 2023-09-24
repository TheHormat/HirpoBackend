from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from wizard.models import Employee
from wizard.models import Project
# class CustomPermissionDenied(APIException):
#     status_code = 403
#     default_detail = '403 Forbidden'
#     default_code = 'forbidden'
class IsCompanyLead(BasePermission):
    message = "besuperuser"
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Project.objects.filter(companyLeader=request.user).exists():
                return True
        return bool(request.user and request.user.employee.is_systemadmin == True)

class HasEmployeeOrNot(BasePermission):
    message = "besuperuser"
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Employee.objects.filter(user=request.user).exists():
                return True
        return False
        



    