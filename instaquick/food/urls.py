from django.urls import path
from . import views

app_name = "food"

urlpatterns = [
    path("", views.food_list, name="list"),
    path("restaurant/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
]
