
from website.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import markdown

#----------------------------- DashBoard --------------------------------------------------------------

def dashboard(request):
    return render(request, 'dashboard.html')






#******************************************** Employee Section *****************************************************
 
#------------------------------ List of Employee ---------------------
def employeeView(request):
    employees = Employee.objects.all().order_by('-created_at')

    return render(request, 'employee/employeelist.html', {'employees': employees})


#------------------------------ Add Employee -------------------------
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

    return render(request, 'employee/addemployee.html', {'choices': choices})

#------------------------------ Delete Employe -----------------------
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

#------------------------------ Edit Employe --------------------------
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
            return render(request, 'employee/edit_employee.html', {'emp': emp, 'choices': choices})
    except Exception as e:
        print(e)
        messages.error(request, 'Employee Not Found')
        return redirect('/staff/employee/')             

#******************************************** End of Employee Section ********************************************





#******************************************** Doctor Section *****************************************************

#-------------------------------------- List of Doctor ----------------------
def doctorView(request):
    doctor = DoctorModel.objects.all().order_by('-created_at')

    return render(request, 'doctors/doctorlist.html', {'doctorview': doctor})


#-------------------------------------- Add Doctor ---------------------------
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
                'role': request.POST['role'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            doc_obj = DoctorModel(**form)
            doc_obj.set_password(form['password'])
            doc_obj.save()
            return redirect('/staff/doctors/')
        else:
            return render(request, 'doctors/addDoctor.html', {'choices': choices})


    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'doctors/addDoctor.html', {'choices': choices})


#-------------------------------------- Edit Doctor ---------------------------
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
                   'role': request.POST['role'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            for key, value in form.items():
                setattr(doc, key, value)
            doc.save()
            messages.success(request, 'Employee Updated Successfully')
            return redirect('/staff/doctors/')
        else:
            return render(request, 'doctors/editDoctor.html', {'emp': doc, 'choices': choices})
    except Exception as e:
        print(e)
        messages.error(request, 'Doctor Not Found')
        return redirect('/staff/doctors/')             

#-------------------------------------- Delete Doctor --------------------------
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


#******************************************** End of Doctor Section ********************************************






#******************************************** Doctor Schedule Section ********************************************

#-------------------------------------- List of Doctor Schedule -------------------
def doctorScheduleView(request):
    doctorsched = DoctorSchedule.objects.all().order_by('-created_at')

    return render(request, 'doctorSchedule/doctorSchedule.html', {'docshed': doctorsched})


#-------------------------------------- Add Doctor Schedule ------------------------
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

            return render(request, 'doctorSchedule/addDoctorschedule.html', {'doc_choices': doctor_objs, 'choices': choices})    

    except Exception as e:
        
        print("---------------")
        print(e)
    
    messages.error(request, 'Schedule Not Added')
    return redirect('/staff/doctorSchedule/')

#-------------------------------------- Generate Slots -----------------------------
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

#******************************************** End of Doctor Schedule Section ********************************************



#******************************************** Appointment Section ********************************************

#-------------------------------------- List of Appointment -----------------------------
def viewAppointment(request):
    appointment = BookAppointment.objects.all().order_by('-created')
    return render(request, 'appointment/viewAppointment.html', {'appointment': appointment})


#-------------------------------------- Specific Appointment Details----------------------
def viewParticularAppointment(request,id):
    appointment = BookAppointment.objects.get(conformation_id=id)
    return render(request, 'appointment/viewParticularAppointment.html', {'appointment': appointment})

#******************************************** End of Appointment Section ********************************************






#********************************************  Blogs Section ********************************************

#-------------------------------------- List of Blogs -------------------------------

def viewAllBlogs(request):
    blogs = Blog.objects.all().order_by('-created')
    return render(request, 'blogs/total_blogs.html', {'blogs': blogs})


#-------------------------------------- Add Blog -------------------------------------

def addBlog(request):
    try:

        if request.method == 'POST':
            author = DoctorModel.objects.get(empid=request.POST['author'])
        #     md = markdown.Markdown(extensions=['extra'])
        #     body_blog = md.convert(request.POST['body_blog'])
            body_blog = request.POST['body_blog']
            form = {
                'title': request.POST['title'],
                'body': body_blog,
               
                'status': request.POST['status'],
                'author': author,
            
            }
            if request.FILES:
                form['image'] = request.FILES['image']

        
            blog_obj = Blog(**form)
            blog_obj.save()
            print("*"*50)
            messages.success(request, 'Blog Added Successfully')
            return redirect('/staff/blogs/')
        else:
        
            statuschoice=(('draft', 'Draft'),('published', 'Published'))
            doctor_objs = DoctorModel.objects.filter(status='active')

            return render(request, 'blogs/addBlog.html', {'choices': statuschoice, 'doc_choices': doctor_objs})
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Added')
        return redirect('/staff/blogs/')

#-------------------------------------- View Specific Blog ----------------------------

def view_blog_part(request,id):
    blog = Blog.objects.get(id=id)
    return render(request, 'blogs/view_blog_part.html', {'blog': blog})

#-------------------------------------- Delete Blog ------------------------------------

def deleteBlog(request,id):
    try:
        blog = Blog.objects.get(id=id)
        blog.delete()
        messages.success(request, 'Blog Deleted Successfully')
        return redirect('/staff/blogs/')
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Deleted')
        return redirect('/staff/blogs/')

#-------------------------------------- Edit Blog ----------------------------------------

def editBlog(request,id):
    try:
        blog = Blog.objects.get(id=id)
        if request.method == 'POST':
          
            # md = markdown.Markdown(extensions=['extra'])
            # body_blog = md.convert(request.POST['body_blog'])       
            body_blog = request.POST['body_blog']                 
            form = {
                'title': request.POST['title'],
                'body': body_blog,
                'status': request.POST['status'],
            
            }
            for key, value in form.items():
                setattr(blog, key, value)
            blog.save()
            messages.success(request, 'Blog Updated Successfully')
            return redirect('/staff/blogs/'+str(id))
        else:
            statuschoice=(('draft', 'Draft'),('published', 'Published'))
            doctor_objs = DoctorModel.objects.filter(status='active')            
            return render(request, 'blogs/editBlog.html', {'blog': blog, 'choices': statuschoice, 'doc_choices': doctor_objs})
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Updated')
        return redirect('/staff/blogs/')        

#******************************************** End of Blogs Section ********************************************        