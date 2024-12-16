from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from django.contrib.auth import authenticate

class GetAllHalls(generics.ListAPIView):
    queryset=Hall.objects.all()
    serializer_class=HallSerializer

class Register(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':403,"message":"Invalid Details"})
        
        user=serializer.save()
        refresh= RefreshToken.for_user(user)

        return Response({'status':200, 'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token),'message':"User Registered Succesfully"})

class Login (APIView):

    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)

        if user is None:
            return Response({'status':401,'message':"Invalid Credentials"})
        
        refresh= RefreshToken.for_user(user)
        return Response({'status':200, 'payload':user.username ,'refresh':str(refresh), 'access':str(refresh.access_token), 'message':'Login Succesful'})



from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission

class IsAdminorSameUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and  request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        
        return request.user and  request.user.is_authenticated and ( request.user.is_staff or obj.instance.user==request.user)

class CreateHall(generics.CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]

    queryset=Hall.objects.all()
    serializer_class=HallSerializer

class PendingRequest(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]
    
    def get(self,request):
        schedule=Schedule.objects.filter(booking_status='pending').order_by('timeofreq')
        schedule=ScheduleSerializer(schedule,many=True)
        return Response({'status':200,'payload':schedule.data})

class ChangeBookingStatus(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]
    
    def patch(self,request,id):
        schedule=Schedule.objects.get(id=id)
        
        if not schedule:
            return Response({'status':400,'message':"No such event"})
        data = {'booking_status': request.data.get('booking_status')}
        schedule=ScheduleSerializer(schedule,data=data,partial=True)
        if schedule.is_valid():
            schedule.save()
        return Response({"status": 200,  "message": f"Booking status is {schedule.instance.booking_status}"})

class BookHall(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        data=request.data
        # print(data)
        if 'hallname' in data and data['hallname']:
            hallname=data['hallname']
            if hallname:
                hall=Hall.objects.get(name=hallname)
                if not hall:
                    return Response({'status':400,'message':"Hall Does not exist"})
                data['hall']=hall.id
        # print(hall)
        data['user']=request.user.id
        data['booking_status']='pending'
        # print (data)
        serializer=ScheduleSerializer(data=data)
        # print (serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data, "message": "Hall request sent"})
        else:
            return Response({"status": 400, "message": "Hall not available", "errors": serializer.errors})


class ChangeBookingDetails(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminorSameUser]
    
    def get(self,request,id):
        schedule=Schedule.objects.get(id=id)
        
        if not schedule:
            return Response({'status':400,'message':"No such event"})
        
        schedule=ScheduleSerializer(schedule)
        return Response({'status':400, 'payload':schedule.data, 'message':"No such event"})

    def patch(self,request,id):
        schedule=Schedule.objects.get(id=id)
        
        if not schedule:
            return Response({'status':400,'message':"No such event"})
        
        
        if 'booking_status' in request.data and request.data['booking_status']:
            return Response({'status':400,'message':"Cannot change booking status"})

        schedule.booking_status='pending'
            
        
        data=request.data
        if 'hallname' in data and data['hallname']:
            hallname=data['hallname']
            if hallname:
                hall=Hall.objects.get(name=hallname)
                if not hall:
                    return Response({'status':400,'message':"Hall Does not exist"})
                data['hall']=hall.id

        schedule=ScheduleSerializer(schedule,data,partial=True)

        if schedule.is_valid():
            schedule.save()
            return Response({'status':200,'message':"Changes saved"})
        return Response({'status': 400, 'message':"Updates not saved" })

    def delete(self,request,id):
        schedule=Schedule.objects.get(id=id)
        
        if not schedule:
            return Response({'status':400,'message':"No such event"})
        schedule.delete()
        return Response({'status':200,'message':"Deleted Event"})

class GetAllBookings(generics.ListAPIView):
    queryset=Schedule.objects.filter(booking_status='booked')
    serializer_class=ScheduleSerializer

