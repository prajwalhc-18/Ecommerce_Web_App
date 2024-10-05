from django.contrib import admin    
from .models import store1,Cart,ShippingAddress,Order    

class store1_admin(admin.ModelAdmin):  
    list_display=('id','name','price','rating','description','seller_name','image')  
    
admin.site.register(store1,store1_admin)    

@admin.register(Cart)  
class CartAdmin(admin.ModelAdmin):  
    list_display=('product_name','user','quantity','totalprice','timestamp','shipping_address')  
    search_fields=('product_name__name','user__username')  
    list_filter=('timestamp','user')  
    actions=['mark_as_shipped']  
    def mark_as_shipped(self,request,queryset):    
        queryset.update(shipping_address=None)  
    mark_as_shipped.short_description="Mark selected items as shipped"   
    
@admin.register(ShippingAddress)    
class ShippingAddressAdmin(admin.ModelAdmin):  
    list_display=('user','address_line1','city','state','zip_code')  
    search_field=('user__username','address_line1','city','state','zip_code',)  
    
@admin.register(Order)  
class OrderAdmin(admin.ModelAdmin):  
    list_display=('user','shipping_address','total_price','created_at','payment_id')    
    search_fields=('user__username',)  
    list_filter=('created_at',) 