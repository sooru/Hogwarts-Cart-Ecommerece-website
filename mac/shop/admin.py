from django.contrib import admin
from .models import Product,Contact,Order,OrderUpdate
# Register your models here.



admin.site.register(Product)
admin.site.register(Contact)

admin.site.register(Order)
# admin.site.register(OrderUpdate)
@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display=['order_id','update_desc','timestamp']