from .models import *
from rest_framework import serializers



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = ['empid', 'first_name','last_name' ,'designation','experience']

class SlotsSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)


    class Meta:
        model = Slots
        exclude = ('created','updated')
        depth = 1

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookAppointment
        fields = "__all__"       