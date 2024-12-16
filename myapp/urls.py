from .views import *
from django.urls import path,include

urlpatterns = [
    path('',GetAllHalls,name='GetAllHalls'),
    path('login',Login.as_view(),name='Login'),
    path('register',Register.as_view(),name='Register'),
    path('createhall',CreateHall.as_view(),name='CreateHall'),
    path('pendingrequests',PendingRequest.as_view(),name='PendingRequests'),
    path('changebookingstatus/<int:id>',ChangeBookingStatus.as_view(),name='ChangeBookingStatus'),

    path('bookhall',BookHall.as_view(),name='BookHall'),
    path('changebookingdetails/<int:id>',ChangeBookingDetails.as_view(),name='changebookingdetails'),
    path('getallbookings',GetAllBookings.as_view(),name='getallbookings'),
]