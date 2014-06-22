from django.contrib import admin

from models import Discoverer, Dumpster, Address, Overflow

class DumpsterAdmin(admin.ModelAdmin):
    list_display = ('dumpster_type', 'is_full', 'modified_at', 'location')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'zip_code', 'city', 'modified_at')

class DiscovererAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_address', 'points')

class OverflowAdmin(admin.ModelAdmin):
    list_display = ('user', 'dumpster', 'modified_at')

admin.site.register(Discoverer, DiscovererAdmin)
admin.site.register(Dumpster, DumpsterAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Overflow, OverflowAdmin)