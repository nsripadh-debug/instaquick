from django.db import models
from django.contrib.auth.models import User
from food.models import FoodItem
from grocery.models import GroceryItem

CART_TYPES = (("food", "Food"), ("grocery", "Grocery"))
PAYMENT_METHODS = (("COD", "Cash on Delivery"), ("UPI", "UPI"), ("CARD", "Debit/Credit Card"))
ORDER_STATUS = (
    ("placed", "Placed"),
    ("preparing", "Preparing"),
    ("out_for_delivery", "Out for Delivery"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
)


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveIntegerField(default=10)
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    valid_till = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    """Every user gets ONE food cart and ONE grocery cart, kept separate."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    cart_type = models.CharField(max_length=10, choices=CART_TYPES)

    class Meta:
        unique_together = ("user", "cart_type")

    def total(self):
        return sum(i.subtotal() for i in self.items.all())

    def __str__(self):
        return f"{self.user.username} - {self.cart_type} cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, null=True, blank=True)
    grocery_item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def product(self):
        return self.food_item or self.grocery_item

    def subtotal(self):
        return self.product().price * self.quantity

    def __str__(self):
        return f"{self.product()} x {self.quantity}"


class DeliveryPartner(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="delivery_partners/", blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)

    # live location -> updated periodically (e.g. by a driver app or admin)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=10, choices=CART_TYPES)

    delivery_address = models.CharField(max_length=255)
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=25)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, default="pending")  # pending/paid
    transaction_id = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="placed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=150)   # snapshot, so invoice stays correct
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.price * self.quantity


class DeliveryTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="tracking")
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True)

    estimated_minutes = models.PositiveIntegerField(default=30)  # updates as guy moves
    status_message = models.CharField(max_length=150, default="Order placed")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking for order #{self.order_id}"
