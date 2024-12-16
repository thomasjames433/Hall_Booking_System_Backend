from django.contrib import admin
from .models import *
# Register your models here.

class ScheduleInLine(admin.TabularInline):
    model=Schedule
    fields=('date','start_time','end_time','booking_status')
    ordering=['start_time']
    extra=0

    def get_queryset(self, request):
        qset=super().get_queryset(request)  
        return qset.filter(booking_status='booked')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display=('name',)
    inlines=[ScheduleInLine]

admin.site.register(User)