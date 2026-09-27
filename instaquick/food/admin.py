from django.contrib import admin
from .models import Restaurant, FoodCategory, FoodItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "rating")
    search_fields = ("name", "address")


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "category", "price", "is_veg", "is_available", "is_recommended")
    list_filter = ("is_veg", "is_available", "category", "restaurant")
    search_fields = ("name",)
