from django.contrib import admin

# Register your models here.
from .models import Api, Electric, Contact, Order, OrderReport, Cart

admin.site.register(Electric)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderReport)
admin.site.register(Cart)
admin.site.register(Api)