from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth import get_user_model

MyUser = get_user_model()

class Activationcode(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='code')
    activation_code = models.CharField(max_length=40,null=True,blank=True)
    

# class MyUserManager(BaseUserManager):
#     def create_user(self,email,password=None,is_active=True,is_staff=False,is_superuser=False):
#         if not email:
#             raise ValueError("Users must have an email address")
#         user = self.model(
#             email = self.normalize_email(email)
#         )
#         user.set_password(password)
#         user.is_active = is_active
#         user.is_staff = is_staff
#         user.is_superuser = is_superuser
#         user.save(using=self._db)
#         return user

#     def create_superuser(self,email,password=None):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             password=password
#         )
#         user.is_staff=True
#         user.is_superuser=True
#         user.save(using=self._db)
#         return user

# class MyUser(AbstractBaseUser):
#     company_name = models.CharField(max_length=40,verbose_name="Company name", blank=True, null=True)
#     email = models.EmailField(unique=True,max_length=120)
#     name = models.CharField(max_length=40,verbose_name="User name", blank=True, null=True)
#     surname = models.CharField( max_length=40,verbose_name="User surname", blank=True, null=True)
#     slug = models.SlugField(unique=True)

#     activation_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
#     password_reset_code = models.CharField(max_length=120,blank=True,null=True)

#     timestamp = models.DateTimeField(auto_now_add=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'
    
    
#     class Meta:
#         ordering = ['-timestamp']
#         verbose_name = 'MyUser'
#         verbose_name_plural = 'MyUser'

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         if self.surname:
#             return '%s %s'%(self.name,self.surname)
#         return self.name

#     def has_perm(self,perm,obj=None):
#         return self.is_superuser

#     def has_module_perms(self,app_label):
#         return True

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = create_slug_shortcode(size=20, model_=MyUser)
#         return super(MyUser, self).save(*args,**kwargs)