from django.contrib import admin
from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'price')
    

admin.site.register(models.Item, ItemAdmin)