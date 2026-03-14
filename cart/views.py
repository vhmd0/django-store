from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from products.models import Product


def get_cart(request):
    """Get cart from session."""
    cart = request.session.get("cart", {})
    return cart


def save_cart(request, cart):
    """Save cart to session."""
    request.session["cart"] = cart
    request.session.modified = True


def cart_detail(request):
    """Shopping cart page."""
    cart = get_cart(request)
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    context = {
        "products": products,
        "total": total,
        "cart_count": sum(cart.values()),
    }

    return render(request, "cart/cart_detail.html", context)


def cart_add(request, product_id):
    """Add product to cart."""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Get quantity from POST data, default to 1
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    save_cart(request, cart)
    messages.success(request, f"Added {product.name} to your cart.")

    return redirect("cart:detail")


def cart_remove(request, product_id):
    """Remove product from cart."""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(request, cart)
        messages.success(request, f"Removed {product.name} from your cart.")

    return redirect("cart:detail")
