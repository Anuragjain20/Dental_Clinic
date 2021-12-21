from .models import *
from rest_framework import serializers



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'designation','experience']

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