from django.urls import path
from theatre.views import AvailabilityView, CustomUnavailabilityView, SlotView

urlpatterns = [
    path('theatre/<int:id>/availability/', AvailabilityView.as_view(), name='theatre-availability'),
    path('theatre/<int:id>/custom-unavailability/', CustomUnavailabilityView.as_view(), name='custom-unavailability'),
    path('theatre/<int:id>/slots/', SlotView.as_view(), name='theatre-slots'),
]
