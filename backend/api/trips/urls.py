from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip, name='trips'),
    path('<int:trip_id>/', views.trip_detail, name='trip-detail'),
]