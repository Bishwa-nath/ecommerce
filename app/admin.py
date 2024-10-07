from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import *

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'category', 'discounted_price', 'product_image']


@admin.register(Customer)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'mobile', 'city', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'products', 'quantity']

	def products(self, obj):
		link = reverse("admin:app_product_change", args=[obj.product.pk])
		return format_html('<a href="{}">{}</a>', link, obj.product.title)
	

@admin.register(Payment)
class PaymentModleAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_payment_status', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status', 'payment']

	def products(self, obj):
		link = reverse("admin:app_product_change", args=[obj.product.pk])
		return format_html('<a href="{}">{}</a>', link, obj.product.title)
	
	def customers(self, obj):
		link = reverse("admin:app_customer_change", args=[obj.customer.pk])
		return format_html('<a href="{}">{}</a>', link, obj.customer.name)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'product']	

