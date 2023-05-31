from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_login, name="handle_login"),
    path("logout/", views.handle_logout, name="handle_logout"),
    path("create_user/",views.create_user,name='new_user'),
    path("index/", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("products/<int:myid>", views.products, name="product_view"),
    path("cart/",views.cart,name="cart"),
    path("cart_db/",views.cart_table,name="cart_db"),
    path("cart_delete/",views.cart_delete,name="cart_delete"),
    path("minus_db/",views.minus_db,name="minus_db"),
    path("checkout/", views.checkout, name="Checkout"),
    path("invoice/<order_id>", views.invoice, name="invoice"),
    path("history/", views.history, name="history"),
    path("pdf/<order_id>", views.pdf, name="pdf"),
    path("search/", views.search, name="search"),
]
