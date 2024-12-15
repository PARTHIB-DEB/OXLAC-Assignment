from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(WeeklySchedule)
admin.site.register(WeeklyUnavailability)
admin.site.register(CustomUnavailability)
admin.site.register(Slot)