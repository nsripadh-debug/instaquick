from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    image = models.ImageField(upload_to="restaurants/", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    """cakes, bakery, starters, rotis, main course, desserts, drinks etc."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Food categories"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, related_name="items")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="food/", blank=True, null=True)

    is_veg = models.BooleanField(default=True)  # drives the veg/non-veg toggle colour
    is_available = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
