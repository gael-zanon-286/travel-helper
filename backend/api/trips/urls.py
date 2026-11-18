from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.trip, name='trips'),
    path('<int:trip_id>/', views.trip_detail, name='trip-detail'),
    path('<int:trip_id>/locations/', include('api.trips.locations.urls')),
]