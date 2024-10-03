from django.contrib import admin

from buyer.models import PurchaseRequest


# Register your models here.
@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'buyer', 'seller', 'status', 'description', 'created_at'
    )
    search_fields = ('status',)
