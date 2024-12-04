from django.contrib import admin
from .models import (
    Address,
    CartOrder,
    CartOrderItems,
    Category,
    Product,
    ProductImages,
    Wishlist,
    Vendor,
    ProductReview,
)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        "user",
        "title",
        "product_image",
        "price",
        "featured",
        "product_status",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "image"]


class CartsOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "paid_status", "order_date", "product_status"]


class CartsOrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "invoice_no", "item", "images", "qty", "price", "total"]


class ProductRevieAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]


class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "date"]


class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "status"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["title", "vendor_image"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(CartOrder, CartsOrderAdmin)
admin.site.register(CartOrderItems, CartsOrderItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wishlist, WishListAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductReview, ProductRevieAdmin)
