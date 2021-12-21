from django.shortcuts import render
from django.core.mail import send_mail
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import ListAPIView
from .utils import *
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,'home.html',{})


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


def bookingview(request):
    return render(request,'booking.html',{})


def service_page(request):
    return render(request,'service.html',{})                  


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
                doctor = Doctor.objects.get(id=doctor)
                date = datetime.strptime(date, '%Y-%m-%d').date()
                val = check_doctor_is_available(doctor,date)
                print(val)
            if val == False:
                return Response({'status':'not available'})
            
            slot = Slots.objects.filter(date=date,doctor=doctor)    
            print(slot)
            serializer = SlotsSerializer( slot, many=True)
            
                
            return Response(serializer.data)       

        except Exception as e:
            print(e)
            return Response({"Error": "error something went wrong", "status": "500"})


class Doctor_list(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class Book_Appointment(APIView):
    def post(self, request):
        try:
            print("==========================")
            print(request.data)
            obj = Slots.objects.get(id=request.data['slot'])
            if obj.is_available == False:
                return Response({"Error": "Slot is already booked"})
            serializers = AppointmentSerializer(data=request.data)
            if serializers.is_valid():
                
                obj.available_slots -= 1
                if obj.available_slots == 0:
                    obj.is_available = False
                obj.save()


                serializers.save()
                return Response({"Success":"success"})
            else:
                
                return Response(serializers.errors)


        except Exception as e:
            print(e)
            return Response({"Error": "error something went wrong", "status": "500"})