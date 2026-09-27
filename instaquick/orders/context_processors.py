from django.conf import settings
from .models import Cart


def google_maps_key(request):
    """Makes {{ GOOGLE_MAPS_API_KEY }} available in every template."""
    return {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}


def cart_summary(request):
    """Makes {{ food_cart_count }} and {{ grocery_cart_count }} available
    in every template automatically (used in navbar.html cart icons)."""
    food_count = 0
    grocery_count = 0
    if request.user.is_authenticated:
        food_cart = Cart.objects.filter(user=request.user, cart_type="food").first()
        grocery_cart = Cart.objects.filter(user=request.user, cart_type="grocery").first()
        if food_cart:
            food_count = sum(i.quantity for i in food_cart.items.all())
        if grocery_cart:
            grocery_count = sum(i.quantity for i in grocery_cart.items.all())
    return {"food_cart_count": food_count, "grocery_cart_count": grocery_count}
