from django.contrib import admin

from models import Discoverer, Dumpster, Address, Overflow

admin.site.register(Discoverer)
admin.site.register(Dumpster)
admin.site.register(Address)
admin.site.register(Overflow)