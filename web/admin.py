from django.contrib import admin

from web.models import Node, Record, Firmware


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('node', 'moisture', 'date')
    list_filter = ('node', 'date')


admin.site.register(Node)
admin.site.register(Firmware)
