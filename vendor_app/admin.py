from django.contrib import admin
from vendor_app.models import PurchaseOrder, Vendor
# Register your models here.

admin.site.register(PurchaseOrder)
admin.site.register(Vendor)