from django.shortcuts import render, get_object_or_404
from .models import Restaurant, FoodCategory, FoodItem


def food_list(request):
    items = FoodItem.objects.filter(is_available=True)

    veg_filter = request.GET.get("veg")   # "veg" / "nonveg" / None
    category_slug = request.GET.get("category")

    if veg_filter == "veg":
        items = items.filter(is_veg=True)
    elif veg_filter == "nonveg":
        items = items.filter(is_veg=False)

    if category_slug:
        items = items.filter(category__slug=category_slug)

    context = {
        "items": items,
        "categories": FoodCategory.objects.all(),
        "veg_filter": veg_filter,
        "active_category": category_slug,
    }
    return render(request, "food/food_list.html", context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.items.filter(is_available=True)
    return render(request, "food/restaurant_detail.html", {
        "restaurant": restaurant, "items": items
    })
