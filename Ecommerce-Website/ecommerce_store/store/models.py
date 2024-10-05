from django.db import models    
from django.contrib.auth.models import User                                     
              

# Create your models here.
class store1(models.Model):
    name=models.CharField(max_length=100)  
    price=models.DecimalField(max_digits=10,decimal_places=2)  
    rating=models.FloatField()      
    description = models.TextField()   
    seller_name=models.CharField(max_length=100)           
    image=models.ImageField(upload_to='media')      
    def __str__(self):    
        return self.name                    
    
class ShippingAddress(models.Model):    
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    address_line1=models.CharField(max_length=255)  
    address_line2=models.CharField(max_length=255,blank=True, null=True)  
    city=models.CharField(max_length=100)  
    state=models.CharField(max_length=100)  
    zip_code=models.CharField(max_length=20)  
    def __str__(self):  
        return f"{self.address_line1},{self.city},{self.state},{self.zip_code}"  
    
class Order(models.Model):  
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True,blank=True)  
    total_price=models.FloatField(default=0)   
    created_at=models.DateTimeField(auto_now_add=True)  
    payment_id=models.CharField(max_length=255,blank=True,null=True)  
    
    def save(self,*args,**kwargs):  
        if not self.pk:   
            super(Order,self).save(*args,**kwargs)     
            cart_items=Cart.objects.filter(user=self.user,order__isnull=True) 
            for cart_item in cart_items:  
                cart_item.order=self       
                cart_item.save()  
            self.total_price=sum(item.totalprice for item in Cart.objects.filter(order=self))  
            self.save()   
        super(Order,self).save(*args,**kwargs)    
    def __str__(self):  
        return f"Order #{self.pk}"    
    
class Cart(models.Model):  
    cart_id=models.CharField(max_length=250,blank=True)  
    product_name=models.ForeignKey(store1,on_delete=models.CASCADE)  
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    quantity=models.IntegerField(default=1)  
    totalprice=models.FloatField(default=0)  
    timestamp = models.DateTimeField(auto_now_add=True)  
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True,related_name="cart_items")  
    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True,blank=True) 