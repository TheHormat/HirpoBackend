from django.db import models
from account.utils import create_slug_shortcode
from django.contrib.auth import get_user, get_user_model
from datetime import date
from django.db.models import Q

today = date.today()

User = get_user_model()

skilltype=(
    ('Soft','Soft'),
    ('Hard','Hard'),
)

industries=(
    ('IT','IT'),
    ('Construction','Construction'),
)
 

class Hirponorms(models.Model):
    skill = models.CharField(max_length=255,verbose_name='Bacariq')
    skilltype = models.CharField(choices=skilltype,max_length=5,null=True,blank=True,verbose_name='skilltype')
    department = models.CharField(max_length=255,verbose_name='Department')
    position = models.CharField(max_length=255,verbose_name='Position')
    norm = models.IntegerField()
    
    def __str__(self):
        return f'{self.department}-{self.position}-{self.skill}'
    


"""{"companyleader": 110, "project_name": "TEST","employee_number": 25, "industry": "IT", "objects": [{"name": "TEST","employee_number":3},{"name": "TEWST","employee_number":3},{"name": "TESTT","employee_number":3}]}"""

class Project(models.Model):
    project_name = models.CharField(max_length=255,verbose_name='Project adi')
    employee_number = models.PositiveIntegerField(verbose_name='Isci sayi')
    industry = models.CharField(max_length=30,  verbose_name='Company field')
    companyLeader = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="project")
    
    def __str__(self):
        return f'{self.project_name}'
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        
    
    
    
class Period(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="period")
    period_number= models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    period_position = models.CharField(max_length=150,null=True,blank=True)
    
    def __str__(self):
        return self.project.project_name
    
    class Meta:
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'


class Evaluation_frequency(models.Model):
    freq_number = models.SmallIntegerField(null=True,blank=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE,related_name='frequency')
    start_date = models.DateField()
    end_date = models.DateField()
    evalution_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.freq_number)
    
    class Meta:
        verbose_name = 'Frequency'
        verbose_name_plural = 'Frequencies'
        
    def get_frequency_scores(self):
        skills = UserSkill.objects.filter(card__evaluation_frequency = self)
        total,weight = 0,0
        for x in skills:
            total += x.price/x.skill.norm*x.skill.weight
            weight += x.skill.weight
        total = total/weight*100
        return {'total':total}     
       

    
class ProjectDepartment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True,related_name='departments')
    name = models.CharField(max_length=255,verbose_name='Department adi')
    description = models.TextField(verbose_name='Department haqqinda',null=True,blank=True)
    employee_number = models.PositiveIntegerField(null=True,blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        
    def get_allSkills(self):
        Skills = []
        for y in self.departmentpositions.all():
            
            for x in MainSkill.objects.filter(position=y):
                Skills.append({"id":x.id,'skillype':x.skilltype,"name":x.name,'skilltype':x.skilltype,"weight":x.weight,'position':x.position.id})
        return Skills

          
    def get_compatencies(self):
        comptencies = []
        position = DepartmentPosition.objects.filter(department=self)
        for y in position:
            for c in MainSkill.objects.filter(position=y):
                comptencies.append({'norm':c.norm,'skilltype':c.skilltype,"id":c.id,"department":{"name":c.position.department.name,"id":c.position.department.id},'skill':{"name":c.name,'skilltype':c.skilltype,"id":c.id},'position':{'name':c.position.name,'id':c.position.id}})
        return comptencies
    

class DepartmentPosition(models.Model):
    name = models.CharField(max_length=20,verbose_name='Position leveli',null=True,blank=True)    
    description = models.TextField(verbose_name='Position haqqinda',null=True,blank=True)
    department = models.ForeignKey(ProjectDepartment,on_delete=models.CASCADE,null=True,blank=True,related_name='departmentpositions')
    report_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    report_to_ceo = models.BooleanField(null=True,blank=True,default=False)
    positionlevel = models.CharField(max_length=120,null=True,blank=True)
    
    def __str__(self):
        
        if self.department:
            return f"{self.name} {self.department.name}"
        else:
            return self.name
    
    class Meta:
        verbose_name = 'Position Level'
        verbose_name_plural = 'Position Levels'
        ordering = ['name']
        

    
class MainSkill(models.Model):
    name = models.CharField(max_length=255,verbose_name='Bacariq adi')
    skilltype = models.CharField(choices=skilltype,max_length=5,null=True,blank=True,verbose_name='skilltype')
    description = models.TextField(null=True,blank=True)
    position = models.ForeignKey(DepartmentPosition, on_delete=models.CASCADE,related_name='myskills')
    norm = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.name}-{self.position.name}' 
       
    class Meta:
        verbose_name = 'Main SKill'
        verbose_name_plural = 'Main Skills'
        
        
        
    # def save(self, *args, **kwargs):
    #     oldobject = SkillNorm.objects.filter(position__name=self.position.name,skill__name=self.skill.name,position__department=self.position.department)
    #     print(self.position,self.skill)

    #     if oldobject.exists():
    #         print(oldobject)
    #         oldobject.delete()
    #     super(SkillNorm, self).save(*args, **kwargs)
    

class Employee(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,related_name='employee',on_delete=models.SET_NULL)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='employee',null=True,blank=True)
    first_name = models.CharField(max_length=20,verbose_name='User adi',null=True,blank=True)
    last_name = models.CharField(max_length=20,verbose_name='User soyadi',null=True,blank=True)
    position = models.ForeignKey(DepartmentPosition,related_name='user',on_delete=models.CASCADE,verbose_name='position level',null=True,blank=True)
    salary = models.PositiveIntegerField(null=True,blank=True)
    hire_date = models.DateField(null=True,blank=True,auto_now_add=True)
    is_systemadmin = models.BooleanField(default=False,null=True,blank=True)
    phone = models.PositiveIntegerField(null=True,blank=True)
    report_to = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.user}-'
    
    class Meta:
        ordering = ['-position']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def delete(self, *args, **kwargs):
        parent = self.parent
        super().delete(*args, **kwargs)
        parent.delete_if_child_deleted()

    def delete_if_child_deleted(self):
        if self.parent.childmodel_set.count() == 0:
            self.parent.delete()
    
    def get_compatencies(self):
        comptencies = []
        for c in MainSkill.objects.filter(position=self.position):
            comptencies.append({'weight':c.weight,"skilltype":c.skilltype,'norm':c.norm,"id":c.id,'skill':{"name":c.name,"id":c.id}})
        return comptencies
    
    # def get_score_for_userperformancepanel(self):
    #     data={}
    #     for y in self.myscore.filter(evalution__start_date__lte=today,evalution__end_date__gte=today):
    #         for x in y.comptency.all():
    #             if y.employee.position.positionlevel.report_to == y.rater.position.positionlevel:
    #                 data['manager'+'-'+y.evaluation_frequency.freq_number+'-'+x.name] = 
    
    def get_all_scores(self):
        ceo,cowerker,selfscore,sub,manager = {},{},{},{},{}
        for y in self.myscore.filter(evaluation_frequency__start_date__lte=today,evaluation_frequency__end_date__gte=today):
            for x in y.comptency.all():
                try:
                    if y.rater.is_systemadmin and y.rater != y.employee:
                        if ceo.get(x.skill.name):
                            ceo[x.skill.name] += (x.price/x.skill.norm*100)
                            ceo[x.skill.name+'say'] +=1
                        else:
                            ceo[x.skill.name] = (x.price/x.skill.norm*100)
                            ceo[x.skill.name+'say'] = 1
                    elif y.employee.position.report_to == y.rater:
                        if manager.get(x.skill.name):
                            manager[x.skill.name] += (x.price/x.skill.norm*100)
                            manager[x.skill.name+'say'] +=1
                        else:
                            manager[x.skill.name] = (x.price/x.skill.norm*100)
                            manager[x.skill.name+'say'] = 1
                       
                    elif y.employee == y.rater:
                        if selfscore.get(x.skill.name):
                            selfscore[x.skill.name] += (x.price/x.skill.norm*100)
                            selfscore[x.skill.name+'say'] +=1
                        else:
                            selfscore[x.skill.name] = (x.price/x.skill.norm*100)
                            selfscore[x.skill.name+'say'] = 1
                        
                    elif y.employee == y.rater.position.report_to:
                        if sub.get(x.skill.name):
                            sub[x.skill.name] += (x.price/x.skill.norm*100)
                            sub[x.skill.name+'say'] +=1
                        else:
                            sub[x.skill.name] = (x.price/x.skill.norm*100)
                            sub[x.skill.name+'say'] = 1     
                    elif y.employee.position.report_to == y.rater.position.report_to:
                  
                        if cowerker.get(x.skill.name):
                            print(x.skill.name,'2')
                            cowerker[x.skill.name] += (x.price/x.skill.norm*100)
                            cowerker[x.skill.name+'say'] +=1
                        else:
                            print(x.skill.name,'3')
                            cowerker[x.skill.name] = (x.price/x.skill.norm*100)
                            cowerker[x.skill.name+'say'] = 1
                       
                    else:
                        pass
                except:
                    pass
        return {"manager":manager,"sub":sub,"cowerker":cowerker,"sub":sub,"selfscore":selfscore}
    
    def get_total_score(self):
        ceo,cowerker,selfscore,sub,manager = [],[],[],[],[]
        total_weight =0
        for y in self.myscore.filter(evaluation_frequency__start_date__lte=today,evaluation_frequency__end_date__gte=today):
            for x in y.comptency.all():
                try:
                    total_weight += x.skill.weight
                    if y.rater.is_systemadmin and y.rater != y.employee:
                        ceo.append((x.price/x.skill.norm*100))
                    elif y.employee.position.report_to == y.rater:
                        manager.append((x.price/x.skill.norm*100))
                    elif y.employee == y.rater:
                        selfscore.append((x.price/x.skill.norm*100))
                    elif y.employee == y.rater.position.report_to:
                        sub.append((x.price/x.skill.norm*100))        
                    elif y.employee.position.report_to == y.rater.position.report_to:
                        cowerker.append((x.price/x.skill.norm*100))
                    else:
                        pass
                except:
                    pass

        result = {}
        if len(ceo)>0:
            result['ceo'] = int(sum(ceo)/len(ceo))
        else:
            result['ceo'] = 0
        if len(cowerker)>0:
            result['cowerker'] = int(sum(cowerker)/len(cowerker))
        else:
            result['cowerker'] = 0
        if len(selfscore)>0:
            result['selfscore'] = int(sum(selfscore)/len(selfscore))
        else:
            result['selfscore'] = 0
        if len(sub)>0:
            result['sub'] = int(sum(sub)/len(sub))
        else:
            result['sub'] = 0
        if len(manager)>0:
            result['manager'] = int(sum(manager)/len(manager))
        else:
            result['manager'] = 0
        

        result['total2'] = result['cowerker']*0.3+result['selfscore']*0.1+result['sub']*0.2+result['manager']*0.4
        
        return result
    
    # def get_hard_goal(self):
    #     hard_goal_skill = {}
    #     for x in MainSkill.objects.all():
    #         if UserSkill.objects.filter(skill=x):

    #             goal = UserSkill.objects.get(skill=x).price/MainSkill.objects.get(skill=x,position=self.position).norm
    #             if x.skilltype == 'Hard':
    #                 hard_goal_skill[x.name] = int(goal*100)
    #     if len(hard_goal_skill)>0:        
    #         hard_goal_skill['average'] = sum(hard_goal_skill.values())/len(hard_goal_skill.values())  
    #     else:
    #         hard_goal_skill['average'] = 0   
    #     return hard_goal_skill
    
    
    # def get_soft_goal(self):
    #     soft_goal_skill = {}
    #     for x in MainSkill.objects.all():
    #         if UserSkill.objects.filter(skill=x):

    #             goal = UserSkill.objects.get(skill=x).price/MainSkill.objects.get(skill=x,position=self.position).norm
    #             if x.skilltype == 'Soft':
    #                 soft_goal_skill[x.name] = int(goal*100)
    #     if len(soft_goal_skill)>0:        
    #         soft_goal_skill['average'] = sum(soft_goal_skill.values())/len(soft_goal_skill.values())
    #     else:
    #         soft_goal_skill['average'] = 0
    #     return soft_goal_skill
    
    # def get_goal(self):    
    #     soft,hard = self.get_soft_goal()['average'],self.get_hard_goal()['average']
    #     if self.position:
    #         if soft == 0 or hard>100:
    #             soft = 100
    #         if hard == 0 or hard>100:
    #             hard = 100
    #         if self.position.name == 'Junior':
    #             return int((soft + hard*3)/4)
    #         if self.position.name == 'Specialist':
    #             return int((soft*4+hard*6)/10)
    #         if self.position.name == 'Senior':
    #             return int((soft+hard)/2)
    #         if self.position.name == 'Manager':
    #             return int((soft*6+hard*4)/10)
    #         if self.position.name == 'TopManager':
    #             return int((soft*3+hard)/4)
    #         return 'Set employee position'    
                    
class AllScores(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='myscore')
    rater = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='mycomment')
    evaluation_frequency = models.ForeignKey(Evaluation_frequency,on_delete=models.CASCADE,related_name='freq')
    is_visible = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.employee.first_name}-qiymetlendiren:{self.rater}'

class UserSkill(models.Model):
    card = models.ForeignKey(AllScores,on_delete=models.CASCADE,related_name='comptency')
    skill = models.ForeignKey(MainSkill, on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    price = models.PositiveIntegerField(null=True,blank=True)
    
    
    def __str__(self):
        return f'who is rated - {self.card.employee.first_name} rater-{self.card.rater.first_name}-{self.skill.name}-{self.price}'
    
    
    # def save(self, *args, **kwargs):
    #     oldobject = UserSkill.objects.filter(card_employee=self.user,skill=self.skill,evaluation_frequency=self.evaluation_frequency)
    #     if oldobject.exists():
    #         print(oldobject)
            
    #         oldobject.delete()
    #     super(UserSkill, self).save(*args, **kwargs)
        

