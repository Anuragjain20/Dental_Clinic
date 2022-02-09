
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from website.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import markdown
from  .utils import *


#----------------------------- DashBoard --------------------------------------------------------------

@login_required(login_url='/staff/login/')
def dashboard(request):
    appointments  = BookAppointment.objects.filter(date__gte =datetime.now()).order_by('-created')
    doctors = DoctorModel.objects.all()
    doct_count = doctors.count()
    blog_count = Blog.published.all().count()
    app_count = BookAppointment.objects.count()

    return render(request, 'dashboard.html',{'appointments':appointments,'doctors':doctors,'doct_count':doct_count,'blog_count':blog_count,'app_count':app_count})
   





#******************************************** Employee Section *****************************************************
 
#------------------------------ List of Employee ---------------------
@login_required(login_url='/staff/login/')
def employeeView(request):
    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
     

        object_list = Employee.objects.all().order_by('-created_at')
        employees = paginatorutils(request,object_list,3)  
        page = request.GET.get('page', 1)
      

        return render(request, 'employee/employeelist.html', {'page_obj': employees,'page':page})
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong')
        return redirect('/staff/dashboard/')

#------------------------------ Add Employee -------------------------
@login_required(login_url='/staff/login/')
def addEmployee(request):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
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

                # 'password': request.POST['password']

            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            emp_obj = Employee(**form)
            emp_obj.set_password(request.POST['password'])
            emp_obj.save()
            return redirect('/staff/employee/')

    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'employee/addemployee.html', {'choices': choices})

#------------------------------ Delete Employe -----------------------
@login_required(login_url='/staff/login/')
def delete_employee(request, slug):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
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
@login_required(login_url='/staff/login/')
def editEmployee(request, slug):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
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
          

               

            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            for key, value in form.items():
                setattr(emp, key, value)

            
            if request.POST['password'] != emp.password:
                emp.set_password(request.POST['password'])
            emp.save()    
            if emp.empid == request.user.empid:
                
                login(request, emp)
                messages.success(request, 'Updated Successfully')
                return redirect('/staff/emp_profile/')

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
@login_required(login_url='/staff/login/')
def doctorView(request):
    if not check_for_admin(request.user):
        messages.error(request, 'You are not authorized to do so')
        return redirect('/staff/dashboard/')

    object_list = DoctorModel.objects.all().order_by('-created_at')
      
    doctor = paginatorutils(request,object_list,5)  
    return render(request, 'doctors/doctorlist.html', {'page_obj': doctor})


#-------------------------------------- Add Doctor ---------------------------
@login_required(login_url='/staff/login/')
def addDoctor(request):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
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
                # 'password': request.POST['password'],
                'fb_link': request.POST['fb_link'],
                'tw_link': request.POST['tw_link'],
                'role': request.POST['role'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            doc_obj = DoctorModel(**form)
            doc_obj.set_password(request.POST['password'])
     
            doc_obj.save()
            return redirect('/staff/doctors/')
        else:
            return render(request, 'doctors/addDoctor.html', {'choices': choices})


    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'doctors/addDoctor.html', {'choices': choices})


#-------------------------------------- Edit Doctor ---------------------------
@login_required(login_url='/staff/login/')
def editDoctor(request, slug):

    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
        doc = DoctorModel.objects.get(slug=slug)
        if check_for_doctor(request.user) and doc.empid != request.user.empid:
            messages.error(request, 'You are not authorized to edit this doctor')
            return redirect('/staff/dashboard/')

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
               
                'fb_link': request.POST['fb_link'],
                'tw_link': request.POST['tw_link'],
                   'role': request.POST['role'],


            }
            if request.FILES:
                form['image'] = request.FILES['profilepic']

            for key, value in form.items():
                setattr(doc, key, value)
            if request.POST['password'] != doc.password:
                doc.set_password(request.POST['password'])
            doc.save()  
            if doc.empid == request.user.empid:
                
                login(request, doc)
                messages.success(request, 'Updated Successfully')
                return redirect('/staff/emp_profile/')
            messages.success(request, 'Updated Successfully')
            return redirect('/staff/doctors/')
        else:
            return render(request, 'doctors/editDoctor.html', {'emp': doc, 'choices': choices})
    except Exception as e:
        print(e)
        messages.error(request, 'Doctor Not Found')
        return redirect('/staff/doctors/')             

#-------------------------------------- Delete Doctor --------------------------
@login_required(login_url='/staff/login/')
def delete_doctor(request, slug):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
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
@login_required(login_url='/staff/login/')
def doctorScheduleView(request):
    if not check_for_admin(request.user) and not check_for_doctor(request.user):
        
        messages.error(request, 'You are not authorized to do so')
        return redirect('/staff/dashboard/')
    if check_for_doctor(request.user):
        doctor = DoctorModel.objects.get(empid=request.user.empid)
        doctorsched = DoctorSchedule.objects.filter(doctor=doctor)
    else:
        doctorsched = DoctorSchedule.objects.all().order_by('-created_at')

    doctorsched =  paginatorutils(request,doctorsched,5)  
    return render(request, 'doctorSchedule/doctorSchedule.html', {'page_obj': doctorsched})


#-------------------------------------- Add Doctor Schedule ------------------------
@login_required(login_url='/staff/login/')
def addDoctorSchedule(request):
    
    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')


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
            if DoctorSchedule.objects.filter(doctor=form['doctor']).filter(Q(start_date__lte=form['start_date']) & Q(end_date__gte=form['start_date'])  ).exists():     
                raise ValueError('Doctor already has a schedule for this date') 
                

            doc_obj = DoctorSchedule(**form)
            doc_obj.save()
            messages.success(request, 'Schedule Added Successfully')
            return redirect('/staff/doctorSchedule/')
        else:
            if check_for_doctor(request.user):
                doctor_objs = DoctorModel.objects.filter(empid=request.user.empid)
            else: 
                doctor_objs = DoctorModel.objects.filter(status='active')

            return render(request, 'doctorSchedule/addDoctorschedule.html', {'doc_choices': doctor_objs, 'choices': choices})    

    except Exception as e:
        
        print("---------------")
        print(e)
        messages.error(request, e)
    
    messages.error(request, 'Schedule Not Added')
    return redirect('/staff/doctorSchedule/')

#-------------------------------------- Generate Slots -----------------------------
@login_required(login_url='/staff/login/')
def gen_slots(request,id):
    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
        docshd = DoctorSchedule.objects.get(id=id)    
        
        if  check_for_doctor(request.user) and request.user.empid != docshd.doctor.empid:
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/doctorSchedule/')
      
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
@login_required(login_url='/staff/login/')
def viewAppointment(request):
    if not check_for_admin(request.user) and not check_for_doctor(request.user):
        messages.error(request, 'You are not authorized to do so')
      
    
        return redirect('/staff/dashboard/')
    if check_for_doctor(request.user):
        doctor = DoctorModel.objects.get(empid=request.user.empid)
        appointment = BookAppointment.objects.filter(doctor=doctor) 
    else:       
        appointment = BookAppointment.objects.all().order_by('-created')
    appointment =  paginatorutils(request,appointment,10)          
    return render(request, 'appointment/viewAppointment.html', {'page_obj': appointment})


#-------------------------------------- Specific Appointment Details----------------------
@login_required(login_url='/staff/login/')
def viewParticularAppointment(request,id):
    if not check_for_admin(request.user) and not check_for_doctor(request.user):
        messages.error(request, 'You are not authorized to do so')
        return redirect('/staff/dashboard/')    
    appointment = BookAppointment.objects.get(conformation_id=id)
    return render(request, 'appointment/viewParticularAppointment.html', {'appointment': appointment})

#******************************************** End of Appointment Section ********************************************






#********************************************  Blogs Section ********************************************

#-------------------------------------- List of Blogs -------------------------------
@login_required(login_url='/staff/login/')
def viewAllBlogs(request):
    if not check_for_admin(request.user) and not check_for_doctor(request.user):
        messages.error(request, 'You are not authorized to do so')
        return redirect('/staff/dashboard/')
    if check_for_doctor(request.user):
        doctor = DoctorModel.objects.get(empid=request.user.empid)
        blogs = Blog.objects.filter(author=doctor)
    else:
        blogs = Blog.objects.all().order_by('-created')
    blogs =  paginatorutils(request,blogs,5)
    return render(request, 'blogs/total_blogs.html', {'page_obj': blogs})


#-------------------------------------- Add Blog -------------------------------------
@login_required(login_url='/staff/login/')
def addBlog(request):
    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')


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
            if check_for_doctor(request.user):
                doctor_objs = DoctorModel.objects.filter(empid=request.user.empid)
            else:
                doctor_objs = DoctorModel.objects.filter(status='active')

        
            statuschoice=(('draft', 'Draft'),('published', 'Published'))

            return render(request, 'blogs/addBlog.html', {'choices': statuschoice, 'doc_choices': doctor_objs})
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Added')
        return redirect('/staff/blogs/')

#-------------------------------------- View Specific Blog ----------------------------
@login_required(login_url='/staff/login/')
def view_blog_part(request,id):
    if not check_for_admin(request.user) and not check_for_doctor(request.user):
        messages.error(request, 'You are not authorized to do so')
        return redirect('/staff/dashboard/')

    blog = Blog.objects.get(id=id)
    return render(request, 'blogs/view_blog_part.html', {'blog': blog})

#-------------------------------------- Delete Blog ------------------------------------
@login_required(login_url='/staff/login/')
def deleteBlog(request,id):
    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
            
        blog = Blog.objects.get(id=id)
        if check_for_doctor(request.user) and request.user.empid != blog.author.empid:
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/blogs/')
   
        blog.delete()
        messages.success(request, 'Blog Deleted Successfully')
        return redirect('/staff/blogs/')
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Deleted')
        return redirect('/staff/blogs/')

#-------------------------------------- Edit Blog ----------------------------------------
@login_required(login_url='/staff/login/')
def editBlog(request,id):
    try:
        if not check_for_admin(request.user) and not check_for_doctor(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
            
        blog = Blog.objects.get(id=id)
        if check_for_doctor(request.user) and request.user.empid != blog.author.empid:
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/blogs/')
     
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
            if check_for_doctor(request.user):
                doctor_objs = DoctorModel.objects.filter(empid=request.user.empid)
            else:
                doctor_objs = DoctorModel.objects.filter(status='active')

            statuschoice=(('draft', 'Draft'),('published', 'Published'))
               
            return render(request, 'blogs/editBlog.html', {'blog': blog, 'choices': statuschoice, 'doc_choices': doctor_objs})
    except Exception as e:
        print(e)
        messages.error(request, 'Blog Not Updated')
        return redirect('/staff/blogs/')        

#******************************************** End of Blogs Section ********************************************        






#********************************************  Authentication Section ********************************************


#-------------------------------------- Login Page -------------------------------------
def login_page(request):
    try:
        if request.method == "POST":
            empid = request.POST['empid']
            password = request.POST['password']
            user = authenticate(request, empid=empid, password=password)
            print("-----------")
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {empid}")
                return redirect('/staff/dashboard/')
            else:
                messages.error(request, "Invalid credentials")
                return redirect('/staff/login/')
        else:
            return render(request, 'authenticating/login.html')
    except Exception as e:
        print(e)
        messages.error(request, 'Login Failed')
        return redirect('/staff/login/')


#-------------------------------------- Logout -------------------------------------
@login_required(login_url='/staff/login/')
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/staff/login/')

#******************************************** End of Authentication Section ********************************************

#********************************************  Profile Section ********************************************


#--------------------------------------Employee Profile Page -------------------------------------
@login_required(login_url='/staff/login/')
def emp_profile(request):
    if  request.user.role == "doctor":
        doctor_obj = DoctorModel.objects.get(empid=request.user.empid)
        return render(request, 'profile/doctor_profile.html', {'obj': doctor_obj})
    obj = Employee.objects.get(empid=request.user.empid)
    return render(request, 'profile/emp_profile.html', {'obj': obj})


#******************************************** End of Profile Section ********************************************    







#******************************************** pricing Section *****************************************************
 
#------------------------------ List of Prices ---------------------
@login_required(login_url='/staff/login/')
def pricingView(request):
    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
     

        object_list = Pricing.objects.all().order_by('-created_at')
        price = paginatorutils(request,object_list,3)  
        page = request.GET.get('page', 1)
      

        return render(request, 'pricing/pricing.html', {'page_obj': price,'page':page})
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong')
        return redirect('/staff/dashboard/')

#------------------------------ Add Price -------------------------
@login_required(login_url='/staff/login/')
def addPrice(request):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
        if request.method == 'POST':
            form = {
                'title': request.POST['title'],
                'price': request.POST['price'],


            }
     
            obj = Pricing(**form)
        
            obj.save()
            return redirect('/staff/pricing/')

    except Exception as e:
        print("---------------")
        print(e)

    return render(request, 'pricing/addpricing.html')

#------------------------------ Delete Price -----------------------
@login_required(login_url='/staff/login/')
def delete_price(request, id):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
        price = Pricing.objects.get(id=id)
        price.delete()

        messages.success(request, 'Service Deleted Successfully')
        return redirect('/staff/pricing/')
    except Exception as e:
        print(e)
        messages.error(request, 'Service Not Deleted')
        return redirect('/staff/pricing/')

# #------------------------------ Edit Price --------------------------
@login_required(login_url='/staff/login/')
def editPrice(request, id):

    try:
        if not check_for_admin(request.user):
            messages.error(request, 'You are not authorized to do so')
            return redirect('/staff/dashboard/')
        price = Pricing.objects.get(id=id)

        if request.method == 'POST':
            form = {
                'title': request.POST['title'],
                'price': request.POST['price'],

            }
      
            for key, value in form.items():
                setattr(price, key, value)
            price.save()
            messages.success(request, 'Price Updated Successfully')
            return redirect('/staff/pricing/')
        else:
            return render(request, 'pricing/edit_price.html', {'price_obj': price})
    except Exception as e:
        print(e)
        messages.error(request, 'Pricing Not Found')
        return redirect('/staff/pricing/')             

#******************************************** End of Pricing Section ********************************************



