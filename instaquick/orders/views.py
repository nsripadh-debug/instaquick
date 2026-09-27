import random
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from food.models import FoodItem
from grocery.models import GroceryItem
from .models import Cart, CartItem, Coupon, Order, OrderItem, DeliveryPartner, DeliveryTracking


# ---------------------------------------------------------------------------
# CART  (food and grocery carts are always kept separate)
# ---------------------------------------------------------------------------
@login_required
def add_to_cart(request, cart_type, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user, cart_type=cart_type)

    if cart_type == "food":
        product = get_object_or_404(FoodItem, id=item_id)
        item, created = CartItem.objects.get_or_create(cart=cart, food_item=product)
    else:
        product = get_object_or_404(GroceryItem, id=item_id)
        item, created = CartItem.objects.get_or_create(cart=cart, grocery_item=product)

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f"{product.name} added to your {cart_type} cart.")
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("orders:cart")


@login_required
def cart_view(request):
    food_cart, _ = Cart.objects.get_or_create(user=request.user, cart_type="food")
    grocery_cart, _ = Cart.objects.get_or_create(user=request.user, cart_type="grocery")
    return render(request, "orders/cart.html", {
        "food_cart": food_cart,
        "grocery_cart": grocery_cart,
    })


# ---------------------------------------------------------------------------
# CHECKOUT / COUPON / PAYMENT
# ---------------------------------------------------------------------------
@login_required
def checkout(request, cart_type):
    cart = get_object_or_404(Cart, user=request.user, cart_type=cart_type)
    coupon = None
    discount = Decimal("0")

    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        payment_method = request.POST.get("payment_method")
        address = request.POST.get("address")
        lat = request.POST.get("latitude") or None
        lng = request.POST.get("longitude") or None

        subtotal = cart.total()

        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
            if coupon and subtotal >= coupon.min_order_value:
                discount = subtotal * Decimal(coupon.discount_percent) / Decimal(100)
            else:
                messages.warning(request, "Coupon not valid for this order.")
                coupon = None

        delivery_fee = Decimal("25")
        total = subtotal - discount + delivery_fee

        order = Order.objects.create(
            customer=request.user,
            order_type=cart_type,
            delivery_address=address,
            delivery_latitude=lat,
            delivery_longitude=lng,
            coupon=coupon,
            subtotal=subtotal,
            discount=discount,
            delivery_fee=delivery_fee,
            total=total,
            payment_method=payment_method,
            # In real UPI/Card flow: create a Razorpay order here, redirect
            # to Razorpay checkout, and only mark "paid" after the webhook
            # confirms payment. COD stays "pending" until delivery.
            payment_status="paid" if payment_method in ("UPI", "CARD") else "pending",
            transaction_id=f"TXN{random.randint(100000, 999999)}" if payment_method != "COD" else "",
        )

        for cart_item in cart.items.select_related():
            product = cart_item.product()
            OrderItem.objects.create(
                order=order, name=product.name,
                price=product.price, quantity=cart_item.quantity,
            )

        # assign a delivery partner + starting ETA
        partner = DeliveryPartner.objects.order_by("?").first()
        DeliveryTracking.objects.create(
            order=order, delivery_partner=partner,
            estimated_minutes=random.randint(20, 45),
            status_message="Order placed",
        )

        cart.items.all().delete()  # empty this cart only
        return redirect("orders:invoice", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart": cart, "cart_type": cart_type,
    })


# ---------------------------------------------------------------------------
# INVOICE  (printable)
# ---------------------------------------------------------------------------
@login_required
def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/invoice.html", {"order": order})


# ---------------------------------------------------------------------------
# LIVE DELIVERY TRACKING
# ---------------------------------------------------------------------------
@login_required
def track_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tracking = getattr(order, "tracking", None)
    return render(request, "orders/track_delivery.html", {
        "order": order, "tracking": tracking,
    })


@login_required
def track_delivery_status(request, order_id):
    """Polled every few seconds by JS on the tracking page to update the
    ETA + delivery guy's live lat/lng on the map without reloading."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tracking = getattr(order, "tracking", None)
    if not tracking:
        return JsonResponse({"error": "no tracking"}, status=404)

    partner = tracking.delivery_partner
    data = {
        "status": tracking.status_message,
        "eta_minutes": tracking.estimated_minutes,
        "partner_name": partner.name if partner else "Unassigned",
        "partner_phone": partner.phone_number if partner else "",
        "latitude": float(partner.current_latitude) if partner and partner.current_latitude else None,
        "longitude": float(partner.current_longitude) if partner and partner.current_longitude else None,
    }
    return JsonResponse(data)
