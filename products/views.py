from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from products.models import Product, Category


def product_list(request):
    """Products page with filtering and pagination."""
    products = Product.objects.select_related("category", "brand").all()

    # Filter by category
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search
    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    # Sort
    sort = request.GET.get("sort", "-created_at")
    if sort in ["price", "-price", "name", "-name", "created_at", "-created_at"]:
        products = products.order_by(sort)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "current_category": category_slug,
        "current_sort": sort,
        "query": query,
    }

    # HTMX partial response for grid updates (search/filter/pagination)
    if request.headers.get("HX-Target") == "product-grid":
        return render(request, "products/partials/product_grid.html", context)

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(
        Product.objects.select_related("category", "brand").prefetch_related("tags"),
        slug=slug,
    )
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)[:4]
    )

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "products/product_detail.html", context)


def category_list(request):
    """Categories listing page."""
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    if request.headers.get("HX-Target") == "category-grid":
        return render(request, "categories/partials/category_list.html", context)

    return render(request, "categories/category_list.html", context)


def category_detail(request, slug):
    """Category detail page with products."""
    category = get_object_or_404(Category, slug=slug)
    products = category.products.select_related("brand").all()

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
    }

    if request.headers.get("HX-Target") == "category-products":
        return render(request, "categories/partials/category_products.html", context)

    return render(request, "categories/category_detail.html", context)
