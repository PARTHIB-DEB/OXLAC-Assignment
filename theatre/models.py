from django.db import models

class Theatre(models.Model):
    name = models.CharField(max_length=100)

class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="screens")
    name = models.CharField(max_length=100)

class WeeklySchedule(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="weekly_schedules")
    day = models.CharField(max_length=20)
    open_time = models.TimeField()
    close_time = models.TimeField()

class WeeklyUnavailability(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="weekly_unavailabilities")
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

class CustomUnavailability(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="custom_unavailabilities")
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

class Slot(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="slots")
    movie = models.CharField(max_length=150)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
