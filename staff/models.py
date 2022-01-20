from distutils.command.upload import upload
import email
from email.mime import image
from operator import mod
from random import choice
from venv import create
from django.db import models


from .managers import Profilemanager
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.text import slugify


choices = {
    'status': (('inactive','Inactive'),('active','Active'),('suspended','Suspended')),
    'gender': (('M',"Male"),('F',"Female"),("O","Other")),
    "role": (('admin','Admin'),('employee','Employee'),('doctor','Doctor')),

}




# Create your models here.
class Profile(AbstractUser):

    username = None
    empid = models.CharField(max_length=50,unique=True,editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50,choices=choices['status'],default='inactive')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender  = models.CharField(max_length=20,choices=choices['gender'])
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to = "media/profile", default = "media/profile/default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=50,choices=choices['role'],default='employee')    
    



    USERNAME_FIELD = 'empid'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = Profilemanager()
 
    def __str__(self) :
        return self.first_name + " " + self.last_name + " " + self.empid


class Employee(Profile):
  

    slug = models.SlugField(max_length=250, unique=True)

    
    #create obj

    #save the emplyee
    def save(self, *args, **kwargs):
        if not self.empid:
            self.empid = "EMP-" + str(uuid.uuid4())[:6]
        self.slug =   slugify(self.first_name + " " + self.last_name + " " + self.empid[-6:]) 
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__()

    class Meta:
        db_table = "employee"
        ordering = ('created_at',)


class DoctorModel(Profile):
  
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()
   
    slug = models.SlugField(max_length=250, unique=True)
    fb_link = models.URLField(blank=True)
    tw_link = models.URLField(blank=True)
   
  

    
    #create obj

    #save the emplyee
    def save(self, *args, **kwargs):
        if not self.empid:
            self.empid = "EMP-" + str(uuid.uuid4())[:6]
        self.slug =   slugify(self.first_name + " " + self.last_name + " " + self.empid[-6:]) 
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__()

    class Meta:
        db_table = "Doctor"
        
        ordering = ('created_at',)

