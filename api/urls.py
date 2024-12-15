from django.urls import path
from ..theatre.views import AvailabilityView, CustomUnavailabilityView, SlotView

urlpatterns = [
    path('<int:id>/availability', AvailabilityView.as_view(), name='theatre-availability'),
    path('<int:id>/custom-unavailability', CustomUnavailabilityView.as_view(), name='custom-unavailability'),
    path('<int:id>/slots', SlotView.as_view(), name='theatre-slots'),
]
