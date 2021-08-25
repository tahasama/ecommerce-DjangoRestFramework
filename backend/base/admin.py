from django.contrib import admin

from base.models import Product, OrderItem, Order, ShippingAddress, Review

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Review)
