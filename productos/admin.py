from django.contrib import admin
from .models import Product,Customer,Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available', 'date')
    readonly_fields= ['date']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address', 'payment_method', 'status', 'date_created', 'status', 'phone')
    readonly_fields= ['date_created']

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
