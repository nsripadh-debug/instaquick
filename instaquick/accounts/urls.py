from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("orders/", views.orders_view, name="orders"),
    path("coupons/", views.coupons_view, name="coupons"),
    path("help/", views.help_view, name="help"),
    path("contact/", views.contact_view, name="contact"),
]
