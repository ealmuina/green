from django.contrib import admin

from web.models import Node, Record, Firmware


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('node', 'moisture', 'date')
    list_filter = ('node', 'date')


@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('node_type', 'version', 'created_at', 'modified_at')
    list_filter = ('node_type',)


admin.site.register(Node)
