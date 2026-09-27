"""
Sits at project root so instaquick/urls.py can import it directly.
Renders the home page: navbar + search + Food section + Grocery section
+ a "Recommended for you" row.
"""
from django.shortcuts import render
from food.models import FoodItem
from grocery.models import GroceryItem


def home(request):
    query = request.GET.get("q", "")

    food_items = FoodItem.objects.filter(is_available=True)
    grocery_items = GroceryItem.objects.filter(is_available=True)

    if query:
        food_items = food_items.filter(name__icontains=query)
        grocery_items = grocery_items.filter(name__icontains=query)

    context = {
        "query": query,
        "food_items": food_items[:8],
        "grocery_items": grocery_items[:8],
        # naive "recommendation" = most recently added + is_recommended flag
        "recommended_food": FoodItem.objects.filter(is_recommended=True)[:6],
        "recommended_grocery": GroceryItem.objects.filter(is_recommended=True)[:6],
    }
    return render(request, "home.html", context)
