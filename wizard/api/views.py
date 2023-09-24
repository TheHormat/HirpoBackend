from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response


import os
import pandas as pd
from wizard.models import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.permissions import IsCompanyLead,HasEmployeeOrNot

#employee goal list
class UserListView(generics.ListAPIView):
  
    queryset = Employee.objects.all()
    serializer_class = EmployeesallSerializer

class CreateProjectWithoutWizardView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self,request):
        data = request.data
        print(data)
        data['companyLeader'] = request.user.id
        project = self.get_serializer(data=data)
        project.is_valid(raise_exception=True)
        project.save()
       
        return Response({"message":"success"},status=201)
    
class CreateProjectView(APIView):

    def post(self,request,format=None):

        for pr in request.user.project.all():
            pr.delete()
     
        object_data = request.data.pop('inputValues')
        data=request.data
        data['companyLeader']=request.user.id
        project_serializer = ProjectSerializer(data=data)
        
        if project_serializer.is_valid(raise_exception=True):
            project = project_serializer.save()
        
            user = request.user
            if Employee.objects.filter(user=user.id).exists():
                myemp = Employee.objects.get(user = user.id)
                myemp.project = project
                myemp.save()
                print(myemp.project)
            for item in list(object_data.keys()):
                name=str(item)
                value=str(object_data[item])
                last_data={"name":name,"employee_number":value,'project':project.id}
                department_serializer = ProjectDepartmentUpdateSerializer(data=last_data)
            
                if department_serializer.is_valid(raise_exception=True):
                    department = department_serializer.save()
                print("department")
                if department.employee_number:
                    employee_number = department.employee_number
                else:
                    employee_number =1
                
                if employee_number == 1:
                    data=[{"name":"Senior",'positionlevel':'Senior'}]
                elif employee_number>1 and employee_number<4:
                    data = [{'name':'Specialist','positionlevel':'Specialist'},{'name':'Senior','positionlevel':'Senior'}]
                elif employee_number>3 and employee_number<6:
                    data = [{'name':'Junior','positionlevel':'Junior'},{'name':'Senior','positionlevel':'Senior'},{'name':'Manager','positionlevel':'Manager'}]
                elif employee_number>5:
                    data = [{'name':'Junior','positionlevel':'Junior'},{'name':'Specialist','positionlevel':'Specialist'},{'name':'Senior','positionlevel':'Senior'},{'name':'Manager','positionlevel':'Manager'}]   

                    
                
                for x in data:
                    print(department.id)
                    x['department']=department.id
                    print(x)
                    position = DepartmentPositionForWizardSerializer(data=x) 
                    
                    if position.is_valid():
                        position.save()
                    else:
                        print(position.errors)
                    print("position")   
        return Response({"message":"success","project":project_serializer.data.get('id')},status=201)
   

"""{"companyleader": "111", "project_name": "ss", "industry": "IT", "employee_number": "22", "inputValues": {"Hr": "22"}}"""

class CreatePositionView(generics.CreateAPIView):
    serializer_class = CreatePositionSerializer
    queryset = DepartmentPosition.objects.all()
    def post(self,request):
   
        positions = DepartmentPosition.objects.filter(department = self.request.data.get('department'))
        for x in positions:
            if x.name == self.request.data.get('name'):
                return Response(status=403)
        print(self.request.data)
        data = request.data
        
        if request.data.get('reports'):
            if request.data.get('reports') == 'Ceo':
                data['report_to_ceo'] = True
            else:
                data['report_to'] = request.data.get('reports')
            
        if request.data.get('positionLevel'):
            data['positionlevel'] = request.data.get('positionLevel')
        serializer = CreatePositionSerializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            print(serializer.errors)            
            return Response(status=400)
            
        
#wizardpositionedit
class PositionUpdateView(APIView):
    def put(self, request, *args, **kwargs):

        position_serializer = DepartmentPosition111Serializer
        print(request.data)
        data = request.data.get('selecteds')
        data2 = request.data.get('objects2')
        data3 = request.data.get('reported')
        print(data,data2,request.data)
        if data:
            for position_data in data:
                serializer = position_serializer(data=position_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        if data2:
            for position_data in data2:
                position = DepartmentPosition.objects.get(id=int(position_data.get('id')))
                if position:            
                    position.delete()

        if data3:
            for x in data3.keys():
                position = DepartmentPosition.objects.get(id = x)
                if data3[x] == 'Ceo':
                    position.report_to_ceo = True
                else:   
                    position.report_to = DepartmentPosition.objects.get(id =data3[x])
                position.save()
        return Response(status=200)

    
class DepartmentPositionListView(generics.ListAPIView):
    serializer_class = ProjectDepartmentSerializer
 
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        user=self.request.user
        
        if user.is_authenticated:
            try:
                project=Project.objects.get(companyLeader=user.id)
            except:
                user = Employee.objects.get(user= user)
                project = user.project
            queryset = queryset.filter(project=project)
            
                  
                    
            return queryset
        
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
   
class ListPositionView(generics.ListAPIView):
    serializer_class = ListPositionFromDepartmentSerializer
 
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        user=self.request.user
        
        if user.is_authenticated:
            try:
                project=Project.objects.get(companyLeader=user.id)
            except:
                user = Employee.objects.get(user= user)
                project = user.project
            queryset = queryset.filter(project=project)
            
                  
                    
            return queryset
        
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
class DepartmentForOrganizitialChart(generics.ListAPIView):
    serializer_class = DepartmentSerializerForOrganizitialChart
  
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        user=self.request.user
        
        if user.is_authenticated:
            project=Project.objects.get(companyLeader=user.id)
            return queryset.filter(project=project)
        
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
                        
                                  
class go_back(APIView):

    def delete(self, request):
        data=request.data
        project = Project.objects.get(id=data.get("project"))
        project.delete()
        return Response({"message":"success"})
    
    
class project_delete(APIView):
  
    def delete(self, request):
        data=request.data
        user = User.objects.get(id=data.get("user_id"))
        employee = Employee.objects.get(user=user)
        projects = employee.project_set.all()
        for project in projects:
            project.delete()
        return Response({"message":"success"})
    
class AddjsonView(APIView):

    def post(self,request):
        data = request.data
        for x in data:
            serializer =  HirponormsSerializer(data=x)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'message':'success'})
        
        
#excellden sqle
class OneTimeVieww(APIView):
 
    def post(self,request):
        df = pd.read_excel('media/Hirpolist.xlsx',usecols=['Department (eng)','Name of competency','Level (1-5)','Type (soft ot hard skills)','Position level'])
        df.fillna('null', inplace=True)
        df.rename(columns={'Level (1-5)': 'norm'}, inplace=True)
        df.rename(columns={'Department (eng)': 'department'}, inplace=True)
        df.rename(columns={'Name of competency': 'skill'}, inplace=True)
        df.rename(columns={'Type (soft ot hard skills)': 'skilltype'}, inplace=True)
        df.rename(columns={'Position level': 'position'}, inplace=True)

        data = df.to_dict(orient='records')

        for x in data:     
            serializer =  HirponormsSerializer(data=x)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        return Response({'message':'success'})
    
#after positions in wizard continue for creating norms
class OneTimeView(APIView):

    def post(self,*args,**kwargs):

        # df = pd.read_excel('Hirpolist.xlsx',usecols=['Department (eng)','Name of competency','Level (1-5)','Type (soft ot hard skills)','Position level'])
        # df.fillna('null', inplace=True)
        # df.rename(columns={'Level (1-5)': 'norm'}, inplace=True)
        # df.rename(columns={'Department (eng)': 'department'}, inplace=True)
        # df.rename(columns={'Name of competency': 'skill'}, inplace=True)
        # df.rename(columns={'Type (soft ot hard skills)': 'skilltype'}, inplace=True)
        # df.rename(columns={'Position level': 'position'}, inplace=True)
        # print('datagettingstage')
        # data = df.to_dict(orient='records')
        data = Hirponorms.objects.all()
        
        user = self.request.user.id
    
        if user:
            project=Project.objects.get(companyLeader=user)


        departments = ProjectDepartment.objects.filter(project=project)
        number = 0

    
        
        for x in departments:
            positions = DepartmentPosition.objects.filter(department=x.id)
            for item in data:
           
                for position in positions:
                    if item.position==position.name and item.department==position.department.name:
                        if not MainSkill.objects.filter(name=item.skill,position=position.id).exists():
                            skill = SkillSerializer(data={'name':item.skill,'position':position.id,'norm':item.norm,'skilltype':item.skilltype})               
                            skill.is_valid(raise_exception=True)
                            skill.save()                       
                            number +=1
                        else:
                            print(MainSkill.objects.filter(name=item.skill,position=position.id),item.skill,position,item.norm)
        # poswe = {}    
        # for x in MainSkill.objects.all():
        #     if x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype in poswe:
        #         poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype] = poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]+1
        #     else:
        #         poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype] = 1
                
        # for x in MainSkill.objects.all():
            
        #     if x.skilltype == 'Soft' and x.position.name == 'Junior':
        #         x.weight = 25/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]

        #     elif x.skilltype == 'Hard' and x.position.name == 'Junior':
        #         x.weight = 75/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     if x.skilltype == 'Soft' and x.position.name == 'Specialist':
        #         x.weight = 40/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     elif x.skilltype == 'Hard' and x.position.name == 'Specialist':
        #         x.weight = 60/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     if x.skilltype == 'Soft' and x.position.name == 'Senior Specialist':
        #         x.weight = 50/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     elif x.skilltype == 'Hard' and x.position.name == 'Senior Specialist':
        #         x.weight = 50/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     if x.skilltype == 'Soft' and x.position.name == 'Manager':
        #         x.weight = 40/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     elif x.skilltype == 'Hard' and x.position.name == 'Manager':
        #         x.weight = 60/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     if x.skilltype == 'Soft' and x.position.name == 'Top Manager':
        #         x.weight = 25/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
        #     elif x.skilltype == 'Hard' and x.position.name == 'Top Manager':
        #         x.weight = 75/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]               
        #     x.save()
                
        return Response({"success":number})

class Get_Weights(APIView):

    def put(self,*args,**kwargs):
        user = self.request.user.id

  
        project=Project.objects.get(companyLeader=user)
        poswe = {}   
        for x in MainSkill.objects.filter(position__department__project = project.id):
            print(x.position.name,x.skilltype,x.position.department.id)
            if x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype in poswe:
                poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype] = poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]+1
            else:
                poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype] = 1
                
        for x in MainSkill.objects.filter(position__department__project = project.id):
            
            if x.skilltype == 'Soft' and x.position.name == 'Junior':
                x.weight = 25/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]

            elif x.skilltype == 'Hard' and x.position.name == 'Junior':
                x.weight = 75/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            if x.skilltype == 'Soft' and x.position.name == 'Specialist':
                x.weight = 40/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            elif x.skilltype == 'Hard' and x.position.name == 'Specialist':
                x.weight = 60/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            if x.skilltype == 'Soft' and x.position.name == 'Senior':
                x.weight = 50/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            elif x.skilltype == 'Hard' and x.position.name == 'Senior':
                x.weight = 50/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            if x.skilltype == 'Soft' and x.position.name == 'Manager':
                x.weight = 40/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            elif x.skilltype == 'Hard' and x.position.name == 'Manager':
                x.weight = 60/poswe[x.position.name+'-'+str(x.position.department.id)+'-'+x.skilltype]
            x.save()
                
        return Response({"message":"success"})
    
class CreateMainSkill(generics.CreateAPIView):
    queryset = MainSkill.objects.all()
    serializer_class = SkillSerializer


    def create(self, request, *args, **kwargs):
        print('1')
        print(request.data)
        data = request.data
        for x in MainSkill.objects.all():
            if x.name == data.get('name') and x.position.id == data.get('position'):
                return Response(status=status.HTTP_409_CONFLICT)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'success'}, status=status.HTTP_201_CREATED)
    
#organizial chart department update
class DepartmentUpdateView(APIView):
   
    def post(self, request, *args, **kwargs):
        department_serializer = department_serializer23
        removed = request.data.get('removedDepartments')
        added = request.data.get('editedDepartments')
        user=request.user
        print(request.data)
        if Project.objects.filter(companyLeader=user).exists():
            project=Project.objects.get(companyLeader=user)
        elif Employee.objects.filter(user = user).exists():
            project = Project.objects.get(employee__project=Employee.objects.get(user = user).id)
        print(project.id,'777')
        for item in removed:
            if ProjectDepartment.objects.filter(id=item.get('id')).exists():
                dp = ProjectDepartment.objects.get(id=item.get('id'))
                if dp:
                    dp.delete()
                
        for item in added:
            print(item)
            item["project"]=project.id
            serializer = department_serializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        return Response({"message":"success"})

#wizardda comptency list view yaratmadan evvel       
class ExcellUploadView(generics.ListAPIView):
    serializer_class = SimpleProjectDepartmentSerializer
   
    
    def get_queryset(self):
        queryset = ProjectDepartment.objects.all()
        data=self.request.user.id
        
        if data:
            try:
                project=Project.objects.get(companyLeader=data)
                
            except:
                user = Employee.objects.get(user= data)
                project = user.project
                print(project)
            return queryset.filter(project=project)   
            
class WizardComptencySaveView(APIView):
    
    def post(self,request):
        print('1')
        data = self.request.data
        print('0')
        print(data)
        for comptency in data.get('createdNorms'):
            
            for x in MainSkill.objects.all():
                
                if comptency.get('skill') == x.name:
                    skltype = x.skilltype
                    break
                
            id = comptency.get('positionId')
            
            
            
            serializer = SkillNormCreateSerializer(data={'norm':comptency.get('newNorm'),"name":comptency.get('skill'),"position":id,'skilltype':skltype})

            if serializer.is_valid():
                serializer.save()
                print('1')
            else:
                print('2')
                print(serializer.errors)
                return Response({'data':serializer.data},status=400)

        for comptency in data.get('editedNorms'):
            comp = MainSkill.objects.get(id=comptency.get('id'))
            serializer = SkillNormUpdateSerializer(comp,data={'norm':comptency.get('norm')})
            if serializer.is_valid():
                serializer.save()
            else:
            
                return Response(status=400)

        for comptency in data.get('removedNorms'):
            myobj = MainSkill.objects.get(id=comptency)
            myobj.delete()
        return Response({'message':'delete success'})
            
class WeightUpdateView(APIView):     

    def put(self, request): 
        serializer = WeightUpdateSerializer   
        data=request.data
        
    
        object = MainSkill.objects.get(id=data.get('id'))
        skills = MainSkill.objects.filter(position=object.position ).exclude(id=data.get('id')) 
        
        cem= 0
        for x in skills:
            cem += x.weight
        print(cem)
        print(data)
        print(data.get('weight'))
        print(object)
        if data.get('weight')==0:
            return Response(status=401)
        if object and cem+float(data.get('weight'))<=100.1:
            myseria = serializer(object,data=data)
            myseria.is_valid(raise_exception=True)
            myseria.save()
        else:
            return Response({"message":object.weight},status=422)
        return Response({'message':'success'})

    
"""{  
    "id": 3,
    "norm": 3,
    "department": 1,
    "position": 73,
    "skill": 1
    }"""        
    
    
class LogoutAPIView(APIView):

    def post(self, request):
        logout_view = LogoutView.as_view()
        response = logout_view(request)

        return Response({'message': 'Logged out successfully'},status=200)

class CheckUserPermission(APIView):

    def get(self, request):
        code = 423
        
        if self.request.user.is_authenticated:
            user = self.request.user
            if Employee.objects.filter(user=user).exists():
                if Employee.objects.get(user=user).is_systemadmin == True:
                    code = 201
                elif Employee.objects.get(user=user).is_systemadmin == False:
                    code = 422
                
            else:
                code = 423
            if Project.objects.filter(companyLeader = user.id).exists():
                code = 200   
        return Response({'code': code},status=code)
      
class AddUser(APIView):
  
    def post(self,request):
        emp = request.data
        if Project.objects.filter(companyLeader=request.user.id).exists():
            project = Project.objects.get(companyLeader=request.user.id)
        else:
            project = Project.objects.get(companyLeader=request.user.employee.project.companyLeader.id)

        print(emp,'22222222222222222222222222222',request.user.id)
        if project:
            data = {
            'username':emp.get('username'),
            'password':emp.get('password'),
            'email':emp.get('email')
            }
            print(data, 'look at password')
            serializer = UserForEmployeeSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            empdata = {
                'project':project.id,
                'user':user.id,
                'position':emp.get('position'),
                'first_name':emp.get('firstName'),
                'last_name':emp.get('lastName'),
                'phone':emp.get('phone'),
                'report_to':emp.get('reportTo'),
            }
            print(empdata)
            employeeSerializer = EmployeeForCreateSerializer(data= empdata)
            employeeSerializer.is_valid(raise_exception=True)
            employeeSerializer.save()
            return Response({"message":"success"})
            
class EmployeeListView(generics.ListAPIView):
   
    serializer_class = EmployeeForListSerializer
    
    def get_queryset(self):
        queryset = []
        data=self.request.user
        if Employee.objects.filter(project__companyLeader=data.id).exists():
            queryset = Employee.objects.filter(project__companyLeader=data)
        else:
            if Project.objects.filter(companyLeader = data.id).exists():
                project = Project.objects.get(companyLeader=data.id)
                queryset = Employee.objects.filter(project = project.id)
        return queryset
    
class EmployeeSingleView(generics.RetrieveAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeForUserListPageSerializer
    lookup_field = 'id'
    
    
    
class EmployeePageView(APIView):

    
    def get(self,request):
        if Employee.objects.filter(user = self.request.user.id):    
            queryset = Employee.objects.get(user = self.request.user.id)
            serializer = EmployeeForUserListPageSerializer
            employee = serializer(queryset)
            return Response(employee.data)
        return Response(status=401)
    
    
    
class PositionSelect(generics.ListAPIView):
 
    serializer_class = DepartmentPosition1112Serializer
    
    def get_queryset(self):
        user=self.request.user
        if DepartmentPosition.objects.filter(department__project__companyLeader_id = user).exists():
            queryset = DepartmentPosition.objects.filter(department__project__companyLeader_id = user.id)
        else:
            queryset = DepartmentPosition.objects.filter(department__project__companyLeader_id = user.employee.project.companyLeader.id)
        
        return queryset
            

        # employeeSerializer.save()
        # return Response({"Status": "success", "data": user_serializer.data}, status=200)


class UserChange(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        data = request.data
        
        
        obj=self.get_object()
        
        serializer = self.serializer_class(data=data,instance=obj,partial=True)
        if data.get('email') == "":
            del data['email'] 
        if data.get('username') == "":
            del data['username']
        if serializer.is_valid():
            
            user = serializer.save()
        else:
            print(serializer.errors
                  )
        return Response({"Status": "success"}, status=201)


class ChangePPView(APIView):
    def post(self, request):

        data = request.data
        employee_id = data.get('data')
        print(employee_id)
        image = request.FILES.get('file')
        employee = Employee.objects.get(id = employee_id)

        image_serializer = EmployeeImageSerializer(employee,data = {'image': image})
        if image_serializer.is_valid():
            image_serializer.save()
            return Response({'message': 'success'})
        else:
            #tour.delete() # delete the created tour object if the image serializer is not valid
            return Response(image_serializer.errors)
        
class HomePageView(generics.ListAPIView):

    serializer_class = HomePageSerializer
    
    def get_queryset(self):

        instance = []
        empexs = Employee.objects.filter(user = self.request.user).exists()
        

        if empexs:
            print('1')
            check=Project.objects.filter(employee=self.request.user.employee.id).exists()
            if check:
               
                instance = [self.request.user.employee.project]

               
                return instance
        if Project.objects.filter(companyLeader = self.request.user.id).exists():       
            instance = Project.objects.filter(companyLeader = self.request.user.id)
                
            return instance
        
        
class PositionAddView(APIView):
    queryset = DepartmentPosition.objects.all()
    
    def put(self,request):
        data= self.request.data
        print(data)
        print(DepartmentPosition.objects.filter(id=data.get('positionlevel')))
        myposition = DepartmentPosition.objects.get(id=data.get('positionlevel'))
        if data.get('reportto'):
            if data.get('reportto') != 'Ceo':
                print(data.get('reportto'),'-------')
                reportto=DepartmentPosition.objects.get(id=data.get('reportto'))
                print(reportto)
                myposition.report_to = reportto
                
            else:
                myposition.report_to_ceo = True
            
        if data.get('description'):
            myposition.description = data.get('description')
        if data.get('name'):
            myposition.name = data.get('name')
        myposition.save()
        print(myposition)
        return Response(status=200)
class PositionDeleteView(generics.RetrieveDestroyAPIView):
    queryset = DepartmentPosition.objects.all()
    serializer_class = DepartmentPosition111Serializer    
    lookup_field = 'id'
    
class MakeVisibledScore(APIView):
    def put(self):
        data = self.request.data
        myscore = AllScores.objects.get(data.id)
        myscore.is_visible = data.is_visible
        myscore.save()
        return Response(status=203)