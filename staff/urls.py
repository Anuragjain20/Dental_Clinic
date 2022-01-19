from django.urls import path


from . import views

app_name = 'staff'



urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('employee/',views.employeeView,name='employee'),
    path('addemployee/',views.addEmployee,name='addemployee'),
    path('employee/delete/<slug:slug>',views.delete_employee,name='delete_employee'),
    path('employee/edit/<slug:slug>',views.editEmployee,name='edit_employee'),
    path('doctors/',views.doctorView,name='doctor'),
    path('adddoctor/',views.addDoctor,name='adddoctor'),
    path('doctors/delete/<slug:slug>',views.delete_doctor,name='delete_doctor'),
    path('doctors/edit/<slug:slug>',views.editDoctor,name='edit_doctor'),
    path('doctorSchedule/',views.doctorScheduleView,name='doctorSchedule'),
    path('addDoctorSchedule/',views.addDoctorSchedule,name='addDoctorSchedule'),
    path('doctorSchedule/gen_slot/<int:id>',views.gen_slots,name='gen_slot'),
    path('viewAppointment/',views.viewAppointment,name='viewAppointment'),
    path('viewAppointment/<id>',views.viewParticularAppointment,name='viewParticularAppointment'),
    path('blogs/',views.viewAllBlogs,name='blog'),
    path("addBlog/",views.addBlog,name='addBlog'),
    path("blogs/<id>",views.view_blog_part,name='view_part_Blog'),
    path("blogs/delete/<id>",views.deleteBlog,name='delete_blog'),
    path("blogs/edit/<id>",views.editBlog,name='edit_blog'),
]
