from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'message', 'rating_stars', 'created_by')
    search_fields = ('message', 'created_by')
    list_display_links = ('message',)
