from django.contrib import admin

from orionframework.media.settings import OnlineDocument


class OnlineDocumentAdmin(admin.ModelAdmin):
    model = OnlineDocument
    list_display = ["id", "title", "origin_url", "origin_type"]
    search_fields = ["title", "origin_url", "origin_type"]
