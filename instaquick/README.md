# InstaQuick – Food + Grocery Delivery (Django)

This project is a full Django starter for an instant food + grocery delivery
site, matching everything you asked for. Below is every step, from an empty
desktop folder to a running site in VS Code, plus where each requested
feature lives in the code.

---

## 1. Create the folder & open in VS Code

```bash
cd ~/Desktop
mkdir instaquick_project
cd instaquick_project
```
Open this folder in VS Code: `File > Open Folder...`
Copy everything from this delivered project into `instaquick_project/`
(you should see `manage.py` at the top level).

## 2. Create a virtual environment (VS Code terminal: Ctrl+`)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
VS Code will prompt "Select this interpreter?" — click **Yes**.

## 3. Install Django + Pillow (Pillow is required for ImageField uploads)

```bash
pip install -r requirements.txt
```

## 4. Apply migrations — this creates db.sqlite3, the database that backs
django-administration and stores every customer, order, product record.

```bash
python manage.py makemigrations accounts food grocery orders
python manage.py migrate
```

## 5. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```
Follow the prompts (username/email/password).

## 6. Run the server

```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** for the site and
**http://127.0.0.1:8000/admin/** for django-administration.

## 7. Add your data in django-administration
Log in at `/admin/` with your superuser and add, in this order:
1. **Food categories** (Cakes, Bakery, Starters, Rotis, Main Course, Desserts, Drinks...)
2. **Restaurants**
3. **Food items** — tick `is_veg` correctly, tick `is_recommended` for a few
4. **Grocery categories** (Home, Electronics, Food, Snacks, Appliances, Face Care, Body Care, Footwear, Fashion...)
5. **Grocery subcategories** (under Fashion: Men, Women; under Men: Shirts, Pants...)
6. **Grocery items**
7. **Delivery partners** (name, phone, vehicle number — these get randomly
   assigned to new orders and shown on the tracking map)
8. **Coupons** (code, discount %, minimum order value)

Every customer who registers on the site automatically gets a row in
**Customer profiles** — that's the "customer details" table you asked about.

---

## 2. Where each feature lives

| Requirement | File(s) |
|---|---|
| django-administration DB holding customer details | `accounts/models.py` (`CustomerProfile`), `accounts/admin.py` |
| Navbar with search bar + login/profile menu | `templates/includes/navbar.html` |
| Footer | `templates/includes/footer.html` |
| `base.html` | `templates/base.html` |
| `home.html` (Food + Grocery sections, recommendations) | `templates/home.html`, `core_views.py` |
| `login.html` / `register.html` | `templates/accounts/login.html`, `register.html`, `accounts/views.py`, `accounts/forms.py` |
| Profile dropdown: profile/help/contact/settings/change details/coupons/orders/logout | `navbar.html` + `accounts/views.py` + `accounts/urls.py` |
| "Not registered? Register" under login button | bottom of `login.html` |
| Register → success message → back to login | `accounts/views.py: register_view` (uses Django `messages`) |
| Explore restaurants / food items | `food/models.py`, `food/views.py`, `templates/food/food_list.html`, `restaurant_detail.html` |
| Separate Food cart & Grocery cart | `orders/models.py: Cart` (`cart_type` field), `templates/orders/cart.html` |
| Veg / Non-veg toggle that changes colour | `templates/food/food_list.html` (`.veg-toggle-btn`), CSS `.active-veg` / `.active-nonveg` |
| Food categories (cakes, bakery, starters...) | `food/models.py: FoodCategory` |
| Grocery categories/subcategories (home, electronics, fashion: men/women: shirts/pants...) | `grocery/models.py: GroceryCategory`, `GrocerySubCategory` |
| Maps for customer address | `templates/accounts/profile.html`, `templates/orders/checkout.html` (Google Maps JS, draggable marker → lat/lng) |
| Payment: COD / UPI / Card / Coupons | `templates/orders/checkout.html`, `orders/models.py: Order`, `orders/views.py: checkout` |
| Print invoice | `templates/orders/invoice.html` (`window.print()` button) |
| Delivery guy tracking map + details + live ETA | `orders/models.py: DeliveryPartner`, `DeliveryTracking`; `templates/orders/track_delivery.html` (polls `orders:track_status` every 5s) |
| Product recommendations | `is_recommended` field on `FoodItem`/`GroceryItem`, shown on `home.html` |
| URLs/views/templates wired together | each app's `urls.py` + `instaquick/urls.py` |

---

## 3. Connecting real Maps & Payments (external services)

**Google Maps** (address picking + live tracking):
1. Go to https://console.cloud.google.com/ → create a project.
2. Enable **Maps JavaScript API**.
3. Create an API key, paste it into `instaquick/settings.py` →
   `GOOGLE_MAPS_API_KEY`.

**UPI / Card payments** (this project stores the choice and creates the
order; wire up a real gateway like Razorpay or Stripe for actual charging):
1. Sign up at https://dashboard.razorpay.com/ (test mode is free).
2. Copy your **Key ID** / **Key Secret** into `settings.py`.
3. In `orders/views.py: checkout`, where the comment says *"create a
   Razorpay order here"*, follow Razorpay's Python quick-start
   (`pip install razorpay`) to open their checkout popup and confirm
   payment via webhook before marking `payment_status="paid"`.
   COD needs no gateway — it's marked "pending" until delivery.

**Live delivery-guy movement**: right now `DeliveryPartner.current_latitude/
longitude` are just DB fields you (or a driver app) update. The tracking
page already polls the server every 5 seconds and moves the map marker +
updates the ETA automatically — you just need something that updates those
two fields periodically (a driver's phone GPS in a real app, or you can
edit them manually in `/admin/` to test).

---

## 4. Handy commands recap

```bash
python manage.py makemigrations   # after changing any models.py
python manage.py migrate          # apply changes to the database
python manage.py createsuperuser  # make an admin login
python manage.py runserver        # start the dev server
```

## 5. Suggested next additions
- Order status auto-updates (Celery/cron job nudging `estimated_minutes` down and `status_message` through placed → preparing → out for delivery → delivered).
- Real payment gateway webhook handling.
- Reviews & ratings per restaurant/item.
- Email/SMS notifications on order placed/delivered.
