from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')



@admin.register(BookAppointment)
class BookAppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email')
    raw_id_fields = ('doctor',)






@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_date', 'start_time', 'end_time')
    list_filter = ('doctor', 'start_date')
    search_fields = ('doctor', 'start_date')
    raw_id_fields = ('doctor',)       


@admin.register(Slots)
class SlotsAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time')
    list_filter = ('doctor', 'date')
    search_fields = ('doctor', 'date')
    raw_id_fields = ('doctor',)

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ( 'created_at', 'updated_at')
    search_fields = ('title', 'price')
