from django.urls import path
from . import views

urlpatterns = [
    path('', views.image, name='image'),
    path('<int:image_id>/', views.image_detail, name='image-detail'),
]