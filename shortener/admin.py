from django.contrib import admin

from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("short_key", "user", "long_url", "created_at", "click_count", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("short_key", "long_url", "user__username")
    readonly_fields = ("created_at", "click_count")
