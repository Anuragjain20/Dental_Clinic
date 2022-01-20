from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import ListAPIView
from .utils import *
from datetime import datetime
import uuid
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from staff.models import *
from .models import *
# Create your views here.



#****************************************** Home Page  ***********************************************
def home(request):
    return render(request,'home.html',{})

#****************************************** End Home Page  ***********************************************


#****************************************** Contact Page  ***********************************************
def contact(request):
    if request.method  == "POST":
        message_name  = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']


        send_mail(
            message_name ,
            message  + "\n" +message_email,
            message_email  ,
            ['anuragjain2rr@gmail.com'],
            fail_silently=False
            
        )
        return render(request,'contact.html',{'message_name':message_name})  

    else:
        return render(request,'contact.html',{})    

#****************************************** End Contact Page  ***********************************************


#****************************************** Service Page  ***********************************************
def service_page(request):
    return render(request,'service.html',{})        

#****************************************** End Service Page  ***********************************************


#****************************************** Blogs Section  ***********************************************



#-------------------- Blog Details ----------------------------
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Blog,
                             slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        print("______________+++++++++++++++++++++")
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        print(name,email,body)
        
        new_comment = Comment.objects.create(
            name=name, email=email, body=body, post=post)
        new_comment.save()    
        print("completed ===================")



    return render(request,
                'detail.html',
                {'post': post,
                'comments': comments,
                'new_comment': new_comment})



#------------------- All Blogs -------------------------------
def all_post(request):
    object_list = Blog.published.all()


    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    print(posts)


    return render(request,
                  'all_blogs.html',
                  {'posts': posts,'page':page})


#****************************************** End Blogs Section  ***********************************************


          

#****************************************** Booking Sections Functionalities ***********************************************


#---------------------- Booking Appointment Page -------------------
def bookingview(request):
    return render(request,'booking.html',{})


#-------------------------------- View Slots  Api -------------------------------------
class SlotsView(APIView):
    def get(self, request):
        try:
            val = False
            date = None
            doctor = None
            if request.GET.get('date'):
                date = request.GET.get('date')
                print(date)
            if request.GET.get('doctor'):
                doctor = request.GET.get('doctor')
                
                print(doctor)
                doctor = DoctorModel.objects.get(empid=doctor)
                date = datetime.strptime(date, '%Y-%m-%d').date()
                val = check_doctor_is_available(doctor,date)
                print(val)
            if val == False:
                return Response({'status':'not available'})
            
            slot = Slots.objects.filter(date=date,doctor=doctor)  

            if  not slot:
                return Response({'status':'not available'})
            
     
            serializer = SlotsSerializer( slot, many=True)

            
                
            return Response(serializer.data)       

        except Exception as e:
            print(e)
            return Response({"Error": "error something went wrong", "status": "500"})

#------------------------------ Doctors List Api -------------------------------------
class Doctor_list(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = DoctorModel.objects.all()

#------------------------ Book Appointment Api -------------------------------------
class Book_Appointment(APIView):
    def post(self, request):
        try:
            print("==========================")
            print(request.data)
            obj = Slots.objects.get(id=request.data['slot'])
            if obj.is_available == False:
                return Response({"Error": "Slot is already booked"})
            request.data['doctor']= DoctorModel.objects.get(empid=request.data['doctor'])  
            request.data['conformation_id']= str(uuid.uuid4()) + "--" + str(obj.available_slots)             
            serializers = AppointmentSerializer(data=request.data)
            if serializers.is_valid():
                
                obj.available_slots -= 1
                if obj.available_slots == 0:
                    obj.is_available = False
                obj.save()
                serializers.save()
                data = {
                    'name':serializers.data['name'],
                    'email':serializers.data['email'],
                    'phone':serializers.data['phone'],
                    'date':serializers.data['date'],
                    
                    'conformationid': serializers.data['conformation_id'],
                
                    'time_slot': str(obj.start_time) + "-" + str(obj.end_time),
                    'doctor': obj.doctor.first_name+" "+obj.doctor.last_name,
                   
                    'message': serializers.data['message'],
                   "STATIC_ROOT": settings.STATIC_URL+"website/img/core-img/logo.png"
                    }
                file_name,ret = save_pdf(data)
                file_name = str(settings.BASE_DIR) + f'/pdfs/{file_name}.pdf'
                print(file_name)
                #sending email with file

                if not ret:
                    return Response({"Error": "error something went wrong"})
                    
                email = EmailMessage(
                    'Appointment Confirmation - Dento',
                    f'Your appointment is confirmed for checkup at Dento on {request.data["date"]}.\nTime Slot is between {data["time_slot"]}.\nPlease check attached pdf for more details.',
                    settings.EMAIL_HOST_USER, [request.data['email']])
                email.attach_file(file_name)
                email.send(fail_silently=False)
    


                

                return Response({"Success":"success"})
            else:
                
                return Response(serializers.errors)


        except Exception as e:
            print(e)
           # return Response({"Error": "error something went wrong", "status": "500"})


#****************************************** End Booking Sections Functionalities ***********************************************




#---------------Extras-----------------
def show_pdf_demo(request):
    data = {
        'name': 'Anurag Jain',
        'conformationid': '123456789',
        'date': '2019-12-12',
        'time_slot': '12:00-12:30',
        'doctor': 'Dr. Anurag Jain',
        'email': 'example@gogle.com',
        'phone': '1234567890',
        'message': 'hello',
        "STATIC_ROOT": settings.STATIC_URL+"website/img/core-img/logo.png"

        
    }
    return render(request,'gen_pdf.html',data)

