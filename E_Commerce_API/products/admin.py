from django.contrib import admin

from .models import Category, Product, Review


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("category_id", "created_at")
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name", "created_at")


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("product_id", "created_at", "updated_at")
    list_display = (
        "name",
        "price",
        "stock_quantity",
        "store_id__store_name",
        "category_id__name",
        "created_at",
    )
    list_filter = ("store_id", "category_id")
    search_fields = ("name", "description")
    ordering = ("name", "price")


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("review_id", "created_at", "updated_at")
    list_display = ("rating", "product__name", "reviewer__username", "created_at")
    list_filter = ("rating", "product_id", "reviewer")
    search_fields = ("comment_title", "comment")
    ordering = ("rating", "created_at")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
