from django.contrib import admin
from .models import Coupon, Cart, CartItem, DeliveryPartner, Order, OrderItem, DeliveryTracking


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "min_order_value", "is_active", "valid_till")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "cart_type")
    inlines = [CartItemInline]


@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "vehicle_number", "rating")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class DeliveryTrackingInline(admin.StackedInline):
    model = DeliveryTracking
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order_type", "total", "payment_method", "payment_status", "status", "created_at")
    list_filter = ("order_type", "payment_method", "payment_status", "status")
    search_fields = ("customer__username", "id")
    inlines = [OrderItemInline, DeliveryTrackingInline]
