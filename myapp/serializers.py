from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','roll_no','password']
        extra_kwargs={
            'password':{'write_only':True},
            'roll_no':{'required':True}
        }

    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return User
    
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hall
        fields=['name']

from rest_framework.exceptions import ValidationError

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Schedule
        fields='__all__'

    def validate(self, data):
        start = data.get('start_time', getattr(self.instance, 'start_time', None))
        end = data.get('end_time', getattr(self.instance, 'end_time', None))
        date = data.get('date', getattr(self.instance, 'date', None))
        hall = data.get('hall', getattr(self.instance, 'hall', None))
        booking_status = data.get('booking_status', getattr(self.instance, 'booking_status', None))

        # Ensure all required fields are present
        if not all([start, end, date, hall]):
            raise ValidationError("Start time, end time, date, and hall are required.")
        
        if end<=start:
            raise ValidationError("End time cannot be lesser than start time")

        overlap=Schedule.objects.filter(
            date=date,
            hall=hall,
            start_time__lte=end, # Existing event starts before the new event ends
            end_time__gte=start,  # Existing event ends after the new event starts
            booking_status='booked'
        )
        if self.instance:
            overlap=overlap.exclude(id=self.instance.id) # if overlap is it with itself,exclude it from overlap

        if overlap.exists():
            raise ValidationError("There is already an event scheduled here")
        
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data=self.validate(validated_data)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance