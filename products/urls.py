from django.urls import path

from products.views import product_list, product_detail, category_list, category_detail

app_name = "products"

urlpatterns = [
    path("", product_list, name="products"),
    path("<slug:slug>/", product_detail, name="product_detail"),
]

categories_urls = [
    path("", category_list, name="categories"),
    path("<slug:slug>/", category_detail, name="category_detail"),
]
