from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<str:cart_type>/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/<str:cart_type>/", views.checkout, name="checkout"),
    path("invoice/<int:order_id>/", views.invoice_view, name="invoice"),
    path("track/<int:order_id>/", views.track_delivery, name="track_delivery"),
    path("track/<int:order_id>/status/", views.track_delivery_status, name="track_status"),
]
