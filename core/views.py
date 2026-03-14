from django.shortcuts import render

from products.models import Category, Product


def home(request):
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.select_related("brand").all()[:8]

    context = {
        "categories": categories,
        "featured_products": featured_products,
    }
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html")
