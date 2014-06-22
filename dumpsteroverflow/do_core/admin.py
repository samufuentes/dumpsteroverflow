from django.contrib import admin

from models import Discoverer, Dumpster, Address, Overflow

class DumpsterAdmin(admin.ModelAdmin):
    list_display = ('dumpster_type', 'is_full', 'modified_at', 'location')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'zip_code', 'city', 'modified_at')

admin.site.register(Discoverer)
admin.site.register(Dumpster, DumpsterAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Overflow)