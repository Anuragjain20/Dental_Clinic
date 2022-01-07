from django.urls import path
from . import views

app_name = 'website'


urlpatterns = [
    path('',views.home,name='home'),
      path('contact',views.contact,name='contact'),
         path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
         path('all_blogs/',views.all_post,name='all_blogs'),
         path('service/',views.service_page,name='service'),
         path('getslots/',views.SlotsView.as_view(),name='getslots'),
         path('doctors/',views.Doctor_list.as_view(),name='doctors'),
         path('bookappointment/',views.Book_Appointment.as_view(),name='bookappointment'),
         path('booking/',views.bookingview,name='booking'),
         path('show_pdf_demo/',views.show_pdf_demo,name='show_pdf_demo'),
]
