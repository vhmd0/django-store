from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product
from orders.models import Order, OrderItem, OrderStatus, PaymentMethod, PaymentStatus


def get_cart(request):
    """Get cart from session."""
    cart = request.session.get("cart", {})
    return cart


def save_cart(request, cart):
    """Save cart to session."""
    request.session["cart"] = cart
    request.session.modified = True


def get_cart_products(request):
    """Get cart products with quantities and totals."""
    cart = get_cart(request)
    products = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            products.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal,
                }
            )
        except Product.DoesNotExist:
            continue

    return products, total


@login_required
def checkout(request):
    """Checkout page - display cart items and shipping form."""
    products, total = get_cart_products(request)

    if not products:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:detail")

    context = {
        "products": products,
        "total": total,
    }
    return render(request, "orders/checkout.html", context)


@login_required
def create_order(request):
    """Create order from cart."""
    if request.method != "POST":
        return redirect("orders:checkout")

    products, total = get_cart_products(request)

    if not products:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:detail")

    shipping_address = request.POST.get("shipping_address", "").strip()
    phone = request.POST.get("phone", "").strip()
    notes = request.POST.get("notes", "").strip()

    if not shipping_address or not phone:
        messages.error(request, "Please provide shipping address and phone number.")
        return redirect("orders:checkout")

    order = Order.objects.create(
        user=request.user,
        status=OrderStatus.PENDING,
        payment_method=PaymentMethod.CASH_ON_DELIVERY,
        payment_status=PaymentStatus.PENDING,
        total_amount=total,
        shipping_address=shipping_address,
        phone=phone,
        notes=notes if notes else None,
    )

    for item in products:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            quantity=item["quantity"],
            price=item["product"].price,
        )

    cart = {}
    save_cart(request, cart)

    return redirect("orders:confirmation", order_id=order.id)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        "order": order,
        "items": order.items.all(),
    }
    return render(request, "orders/order_confirmation.html", context)


@login_required
def order_list(request):
    """User's order history."""
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")

    context = {
        "orders": orders,
    }
    return render(request, "orders/order_list.html", context)


@login_required
def order_detail(request, order_id):
    """Order detail page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        "order": order,
        "items": order.items.all(),
    }
    return render(request, "orders/order_detail.html", context)
