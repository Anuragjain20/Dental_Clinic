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
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('emp_profile/',views.emp_profile,name='emp_profile'),
    path('pricing/',views.pricingView,name='pricingview'),
    path('addpricing/',views.addPrice,name='addPricing'),
    path('pricing/delete/<id>',views.delete_price,name='delete_pricing'),
    path('pricing/edit/<id>',views.editPrice,name='edit_pricing'),

]
