from .models import *
from io import BytesIO
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

from django.template.loader import render_to_string

import uuid
import os





def check_doctor_is_available(doctor, date):
    objs = DoctorSchedule.objects.filter(doctor=doctor)
    for obj in objs:
        
        if obj.start_date  <= date and date <= obj.end_date :
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

def fetch_resources(uri, rel):
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

    return path

def save_pdf(params:dict):
   # template = get_template('gen_pdf.html')
    html = render_to_string('gen_pdf.html', context= params)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result,link_callback=fetch_resources)

    file_name = params['conformationid'] 
    try:
        with open(str(settings.BASE_DIR) + f'/pdfs/{file_name}.pdf', 'wb+') as output:
                
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output,link_callback=fetch_resources)

    except Exception as e:
        print(e)
        return None

    if pdf.err:
        return '',False
    return file_name,True
    
