from django.contrib import admin
from .models import GroceryCategory, GrocerySubCategory, GroceryItem


@admin.register(GroceryCategory)
class GroceryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GrocerySubCategory)
class GrocerySubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "subcategory", "price", "stock", "is_available", "is_recommended")
    list_filter = ("category", "subcategory", "is_available")
    search_fields = ("name",)
