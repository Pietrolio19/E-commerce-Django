from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("/cart/checkout/", views.checkout, name="checkout"),
    path("/cart/checkout/payment/", views.payment, name="payment"),
]
