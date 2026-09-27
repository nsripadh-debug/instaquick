from django.db import models


class GroceryCategory(models.Model):
    """home, electronics, food, snacks, appliances, face care, body care,
    footwear, fashion(men/women) etc."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="emoji or css icon class")

    class Meta:
        verbose_name_plural = "Grocery categories"

    def __str__(self):
        return self.name


class GrocerySubCategory(models.Model):
    """e.g. under Fashion -> Men / Women, under that -> Shirts / Pants"""
    category = models.ForeignKey(GroceryCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=80)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Grocery subcategories"
        unique_together = ("category", "slug")

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class GroceryItem(models.Model):
    category = models.ForeignKey(GroceryCategory, on_delete=models.CASCADE, related_name="items")
    subcategory = models.ForeignKey(GrocerySubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to="grocery/", blank=True, null=True)

    is_available = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
