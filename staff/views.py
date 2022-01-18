
from website.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard.html')


def employeeView(request):
    employees = Employee.objects.all().order_by('-created_at')

    return render(request, 'employeelist.html', {'employees': employees})


def addEmployee(request):

    try:
        if request.method == 'POST':
            form = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'status': request.POST['status'],
                'gender': request.POST['gender'],
                'address': request.POST['address'],
                'role': request.POST['role'],

                'password': request.POST['password']

            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            emp_obj = Employee(**form)
            emp_obj.set_password(form['password'])
            emp_obj.save()
            return redirect('/staff/employee/')

    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'addemployee.html', {'choices': choices})


def delete_employee(request, slug):

    try:
        print(slug)
        emp = Employee.objects.get(slug=slug)
        emp.delete()
        messages.success(request, 'Employee Deleted Successfully')
        return redirect('/staff/employee/')
    except Exception as e:
        print(e)
        messages.error(request, 'Employee Not Deleted')
        return redirect('/staff/employee/')


def editEmployee(request, slug):

    try:
        emp = Employee.objects.get(slug=slug)
        if request.method == 'POST':
            form = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'status': request.POST['status'],
                'gender': request.POST['gender'],
                'address': request.POST['address'],
                'role': request.POST['role'],

                'password': request.POST['password']

            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            for key, value in form.items():
                setattr(emp, key, value)
            emp.save()
            messages.success(request, 'Employee Updated Successfully')
            return redirect('/staff/employee/')
        else:
            return render(request, 'edit_employee.html', {'emp': emp, 'choices': choices})
    except Exception as e:
        print(e)
        messages.error(request, 'Employee Not Found')
        return redirect('/staff/employee/')             
    

def delete_doctor(request, slug):

    try:
        print(slug)
        doc = DoctorModel.objects.get(slug=slug)
        doc.delete()
        messages.success(request, 'Employee Deleted Successfully')
        return redirect('/staff/doctors/')
    except Exception as e:
        print(e)
        messages.error(request, 'Employee Not Deleted')
        return redirect('/staff/doctors/')



def doctorView(request):
    doctor = DoctorModel.objects.all().order_by('-created_at')

    return render(request, 'doctorlist.html', {'doctorview': doctor})


def addDoctor(request):

    try:
        if request.method == 'POST':
            form = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'status': request.POST['status'],
                'gender': request.POST['gender'],
                'address': request.POST['address'],
                'designation': request.POST['designation'],
                'experience':request.POST['experience'],
                'password': request.POST['password'],
                'fb_link': request.POST['fb_link'],
                'tw_link': request.POST['tw_link'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            doc_obj = DoctorModel(**form)
            doc_obj.set_password(form['password'])
            doc_obj.save()
            return redirect('/staff/doctors/')

    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'addDoctor.html', {'choices': choices})



def editDoctor(request, slug):

    try:
        doc = DoctorModel.objects.get(slug=slug)
        if request.method == 'POST':
            form = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'status': request.POST['status'],
                'gender': request.POST['gender'],
                'address': request.POST['address'],
                'designation': request.POST['designation'],
                'experience':request.POST['experience'],
                'password': request.POST['password'],
                'fb_link': request.POST['fb_link'],
                'tw_link': request.POST['tw_link'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            for key, value in form.items():
                setattr(doc, key, value)
            doc.save()
            messages.success(request, 'Employee Updated Successfully')
            return redirect('/staff/doctors/')
        else:
            return render(request, 'editDoctor.html', {'emp': doc, 'choices': choices})
    except Exception as e:
        print(e)
        messages.error(request, 'Doctor Not Found')
        return redirect('/staff/doctors/')             
    
def doctorScheduleView(request):
    doctorsched = DoctorSchedule.objects.all().order_by('-created_at')

    return render(request, 'doctorSchedule.html', {'docshed': doctorsched})

def addDoctorSchedule(request):
    
    try:
        if request.method == 'POST':
            doctor_obj = DoctorModel.objects.get(empid=request.POST['doctor'])
            form = {
                'doctor':doctor_obj,
                'start_date': request.POST['start_date'],
                'end_date': request.POST['end_date'],
                'start_time': request.POST['start_time'],
                'end_time': request.POST['end_time'],
                # 'status': request.POST['status'],


            }
            

            doc_obj = DoctorSchedule(**form)
            doc_obj.save()
            messages.success(request, 'Schedule Added Successfully')
            return redirect('/staff/doctorSchedule/')
        else:
            doctor_objs = DoctorModel.objects.filter(status='active')

            return render(request, 'addDoctorschedule.html', {'doc_choices': doctor_objs, 'choices': choices})    

    except Exception as e:
        
        print("---------------")
        print(e)
    
    messages.error(request, 'Schedule Not Added')
    return redirect('/staff/doctorSchedule/')


def gen_slots(request,id):
    try:
        docshd = DoctorSchedule.objects.get(id=id)
        val = docshd.create_slots()
        if val:
            messages.success(request, 'Slots Created Successfully')
            return redirect('/staff/doctorSchedule/')
        else:
            messages.error(request, 'Slots Not Created')
            return redirect('/staff/doctorSchedule/')
    
    except Exception as e:
        print(e)
        messages.error(request, 'Slots Not Generated')
        return redirect('/staff/doctorSchedule/')

def viewAppointment(request):
    appointment = BookAppointment.objects.all().order_by('-created')
    return render(request, 'viewAppointment.html', {'appointment': appointment})

def viewParticularAppointment(request,id):
    appointment = BookAppointment.objects.get(conformation_id=id)
    return render(request, 'viewParticularAppointment.html', {'appointment': appointment})