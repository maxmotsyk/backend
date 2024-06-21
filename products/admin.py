from django.contrib import admin
from .models import RecommendProduct, Product, ProductDetail, ProductImage, ProductVariation
from reviews.models import Review

class ProductVariation(admin.StackedInline):
    model = ProductVariation
    extra = 1


class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 1


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(RecommendProduct)
class RecommendProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount')
    search_fields = ('title', 'description')
    list_display_links = ('title',)
    inlines = [ProductImageInline, ProductDetailInline, ProductVariation, ReviewInline]
