from .models import *



def check_doctor_is_available(doctor, date):
    objs = DoctorSchedule.objects.filter(doctor=doctor)
    for obj in objs:
        
        if obj.start_date  <= date and date <= obj.end_date:
            return True
    return False

"""
{

"doctor": "1",
"slot" : "1",
"name":"anurag",
"email":"anuragjain2rr@gmail.com",
 "phone":"2344223",
"date":"2021-11-30",
"message":"asdddsS"



}

"""