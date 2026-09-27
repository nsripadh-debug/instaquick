from django.shortcuts import render
from .models import GroceryCategory, GroceryItem


def grocery_list(request):
    items = GroceryItem.objects.filter(is_available=True)

    category_slug = request.GET.get("category")
    if category_slug:
        items = items.filter(category__slug=category_slug)

    context = {
        "items": items,
        "categories": GroceryCategory.objects.prefetch_related("subcategories"),
        "active_category": category_slug,
    }
    return render(request, "grocery/grocery_list.html", context)
