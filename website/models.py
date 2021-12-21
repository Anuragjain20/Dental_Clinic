from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, datetime,timedelta




class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

# Create your models here.

class Blog(models.Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to = 'images/', blank=True)
    slug = models.SlugField(max_length=250,  unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager() 
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('website:post_detail',args=[self.publish.year,self.publish.month,self.publish.day, self.slug])        



class Comment(models.Model):
    post = models.ForeignKey(Blog,
    on_delete=models.CASCADE,
    related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'images/', blank=True)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fb_link = models.URLField(blank=True)
    tw_link = models.URLField(blank=True)
   
    gog_link = models.URLField(blank=True)

    
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'{self.name}'



class Slots(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available_slots = models.IntegerField(default=5)
    is_available = models.BooleanField(default=True)

    
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'{self.doctor} on {self.date} at {self.start_time}'





class BookAppointment(models.Model):



    STATUS_CHOICES = (
            ('pending', 'Pending'),
            ('approved', 'Approved'),   
            ('rejected', 'Rejected'),
            )

    slot= models.ForeignKey(Slots, on_delete=models.CASCADE, related_name='book_appointment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    date = models.DateField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    active = models.BooleanField(default=True)
    
    
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'Appointment by {self.name} on {self.date}'



def create_slots( instance):


    doctor = instance.doctor
    start_date = instance.start_date
    end_date = instance.end_date

    date = start_date

    while date <= end_date:
        start_time = instance.start_time
        end_time = instance.end_time
        
            
        while start_time < end_time:
            st = start_time.strftime("%H:%M")
            e = datetime.strptime(st, "%H:%M") + timedelta(hours=1)
            Slots.objects.create(doctor=doctor, date=date, start_time=start_time, end_time=e.time())
            start_time = (datetime.strptime(st, "%H:%M") + timedelta(hours=1,minutes=30)).time()
        date += timedelta(days=1)


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    #override the save method
    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise ValueError('Start Date cannot be greater than End Date')
        elif self.start_time > self.end_time:
            raise ValueError('Start Time cannot be greater than End Time')
        else:
            # s1= self.start_time.strftime("%H:%M")
            # e1= self.end_time.strftime("%H:%M")
            # #calcutate the total number of slots
            # total_slots = (datetime.strptime(e1, "%H:%M") - datetime.strptime(s1, "%H:%M")).seconds/3600

            # #create a list of slots
            # slots = []
            # for i in range(int(total_slots)):
            #     ti = (datetime.strptime(s1, "%H:%M") + timedelta(minutes=60*i)).time()
            #     if ti > self.end_time :
            #         break
            #     else:
            #         slots.append(ti)
            #         print(slots[i])

               
                #slots.append(datetime.strptime(s1, "%H:%M") + timedelta(minutes=120*i))


            #create slots
            create_slots(self)

            super(DoctorSchedule, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('created_at',)
    
    
    def __str__(self):
        return f'Schedule of {self.doctor}'
