from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import *

class AvailabilityView(APIView):
    def post(self, request, id):
        data = request.data

        # Validate Weekly Schedule
        weekly_schedule = data.get('weekly_schedule', {})
        for day, times in weekly_schedule.items():
            serializer = WeeklyScheduleSerializer(data={
                'day': day,
                'open_time': times.get('open'),
                'close_time': times.get('close')
            })
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate Weekly Unavailability
        weekly_unavailability = data.get('weekly_unavailability', {})
        for day, slots in weekly_unavailability.items():
            for slot in slots:
                serializer = WeeklyUnavailabilitySerializer(data={
                    'day': day,
                    'start_time': slot.get('start'),
                    'end_time': slot.get('end')
                })
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save Weekly Schedule and Unavailability
        theatre = Theatre.objects.get(id=id)
        for day, times in weekly_schedule.items():
            WeeklySchedule.objects.update_or_create(
                theatre=theatre, day=day,
                defaults={'open_time': times['open'], 'close_time': times['close']}
            )
        for day, slots in weekly_unavailability.items():
            for slot in slots:
                WeeklyUnavailability.objects.update_or_create(
                    theatre=theatre, day=day,
                    defaults={'start_time': slot['start'], 'end_time': slot['end']}
                )

        return Response({"message": "Availability updated successfully"}, status=status.HTTP_200_OK)

class CustomUnavailabilityView(APIView):
    def post(self, request, id):
        data = request.data

        # Validate Custom Unavailability
        unavailable_slots = data.get('unavailable_slots', [])
        unavailable_dates = data.get('unavailable_dates', [])

        for slot in unavailable_slots:
            serializer = CustomUnavailabilitySerializer(data=slot)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for date in unavailable_dates:
            serializer = CustomUnavailabilitySerializer(data={
                'screen': data.get('screen_id'),
                'date': date
            })
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save Custom Unavailability
        theatre = Theatre.objects.get(id=id)
        screen_id = data.get('screen_id')
        for slot in unavailable_slots:
            CustomUnavailability.objects.create(
                screen_id=screen_id,
                date=slot['date'],
                start_time=slot['start'],
                end_time=slot['end']
            )
        for date in unavailable_dates:
            CustomUnavailability.objects.create(
                screen_id=screen_id,
                date=date
            )

        return Response({"message": "Custom unavailability updated successfully"}, status=status.HTTP_200_OK)

class SlotView(APIView):
    def get(self, request, id):
        screen_id = request.query_params.get('screen_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not (screen_id and start_date and end_date):
            return Response({"error": "screen_id, start_date, and end_date are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        screen = Screen.objects.filter(id=screen_id, theatre_id=id).first()
        if not screen:
            return Response({"error": "Screen not found."}, status=status.HTTP_404_NOT_FOUND)

        slots = Slot.objects.filter(screen=screen, start_time__date__range=(start_date, end_date))
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
