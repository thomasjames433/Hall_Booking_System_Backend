from django.db import models
from datetime import *
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings

class User(AbstractUser):
    roll_no=models.CharField(max_length=9,unique=True)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username

class Hall(models.Model):
    
    name=models.CharField(max_length=17,unique=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE) 
    date=models.DateField(null=False,blank=False)
    start_time=models.TimeField()
    end_time=models.TimeField()
    bstats=[
        ('booked','Booked'),
        ('available','Available'),
        ('pending','Pending'),
        ('rejected','Rejected'),
    ]
    booking_status=models.CharField(max_length=15, choices=bstats)
    timeofreq= models.DateTimeField(null=True,blank=True,default=datetime.now)
    class Meta:
        ordering=['start_time']
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
