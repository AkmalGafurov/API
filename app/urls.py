from django.urls import path
from .views_fbv import car_list_create, car_detail
from .views_cbv import (
    CarListCreateAPIView,
    CarRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('cars/', car_list_create),
    path('cars/<int:pk>/', car_detail),
    path('cbv/cars/', CarListCreateAPIView.as_view()),
    path('cbv/cars/<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view()),
]



