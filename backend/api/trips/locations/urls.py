from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.location, name='location'),
    path('<int:location_id>/', views.location_detail, name='location-detail'),
    path('<int:location_id>/images/', include('api.trips.locations.images.urls')),
]