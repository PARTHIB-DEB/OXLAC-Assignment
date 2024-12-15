from rest_framework import serializers
from .models import Theatre, Screen, WeeklySchedule, WeeklyUnavailability, CustomUnavailability, Slot

class WeeklyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySchedule
        fields = ['day', 'open_time', 'close_time']

class WeeklyUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyUnavailability
        fields = ['day', 'start_time', 'end_time']

class CustomUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUnavailability
        fields = ['screen', 'date', 'start_time', 'end_time']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['screen', 'movie', 'start_time', 'end_time', 'is_available']
