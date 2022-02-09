from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = ['empid','first_name','last_name','email','phone','role','status']
    list_filter = ['role','status','created_at']
    search_fields = ['empid','first_name','last_name','email','phone']
    list_per_page = 10
 

@admin.register(DoctorModel)
class DoctorAdmin(admin.ModelAdmin):
    
    list_display = ['empid','first_name','last_name','email','phone','status']
    list_filter = ['status','created_at']
    search_fields = ['empid','first_name','last_name','email','phone']
    list_per_page = 10

