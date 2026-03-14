from django.contrib import admin
from django.urls import path, include

from core import views
from products import urls as products_urls
from orders import urls as orders_urls

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.home, name="about"),
    path(
        "products/",
        include((products_urls.urlpatterns, "products"), namespace="products"),
    ),
    path(
        "categories/",
        include((products_urls.categories_urls, "categories"), namespace="categories"),
    ),
    path("wishlist/", views.home, name="wishlist"),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include((orders_urls.urlpatterns, "orders"), namespace="orders")),
    path("users/", include("users.urls", namespace="users")),
)
