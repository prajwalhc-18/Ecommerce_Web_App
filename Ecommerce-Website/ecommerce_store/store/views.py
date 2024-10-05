from django.shortcuts import render,redirect  ,get_object_or_404     
from .models import store1,Cart                                                                                         
from django.contrib.auth.models import User                                  
from django.contrib.auth import authenticate,login,logout  
from .forms import SignupForm  
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm  
    

# Create your views here.
def dashboard(request):  
    object_list=store1.objects.all()   
    
    return render(request,'html/home.html',{'object_list':object_list})  

def product_details(request,id):  
    idd=store1.objects.get(id=id)  
    return render(request,"html/product_details.html",{'i':idd})  


def signup(request):
    if request.method=="POST":  
        fn=SignupForm(request.POST)  
        if fn.is_valid():  
            username=fn.cleaned_data["username"]  
            first_name=fn.cleaned_data["first_name"]  
            last_name=fn.cleaned_data["last_name"]  
            email=fn.cleaned_data["email"]  
            password=fn.cleaned_data["password1"]
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)   
            user.save()  
            return redirect('/login')     
    else:  
        fn=SignupForm(request.POST)    
        print('invalied')  
    return render(request,'html/signup.html',{'form':fn})  

def user_login(request):  
    fn=AuthenticationForm(request.POST)       
    if request.method=='POST':    
        fn=AuthenticationForm(request,data=request.POST)    
        if fn.is_valid():            
            user= fn.cleaned_data['username'] 
            upass=fn.cleaned_data['password']  
        return redirect('/dashboard')  
    return render(request,'html/login.html',{'form':fn})      
def user_logout(request):  
    logout(request)  
    return redirect('/login')  

from django.views.generic import ListView    
from django.db.models import Q  

class SearchResultsView(ListView):  
    model=store1     
    template_name="html/search_results.html"   
    def get_queryset(self):
        query=self.request.GET.get('q')  
        object_list=store1.objects.filter(Q(name__icontains=query) |   Q(description__icontains=query))  
        return object_list       
    def get(self,request,*args,**kwargs):  
        query=self.request.GET.get('q')   
        object_list=self.get_queryset()  
        
        if not object_list:   
            return render(request,"html/not_found.html",{'i':query})     
        return super().get(request,*args,**kwargs)   
    
from django.contrib.auth.decorators import login_required    
@login_required      
def add_to_cart(request):  
    if request.method == 'POST':  
        product_id = request.POST.get('product_id')    
        print(product_id)   
        product=get_object_or_404(store1,id=product_id)  
        cart, created=Cart.objects.get_or_create(user=request.user,product_name=product) 
        cart.quantity +=1   
        cart.totalprice=cart.quantity*product.price                                                   
        cart.save()         
    return redirect('/cart')  
def increment_cart(request,cart_id):    
    cart=get_object_or_404(Cart, id=cart_id ,user=request.user)        
    cart.quantity  +=1    
    cart.totalprice=cart.quantity*cart.product_name.price                        
    cart.save()  
    return redirect('/cart')   

def decrement_cart(request,cart_id):  
    cart=get_object_or_404(Cart,id=cart_id,user=request.user)    
    if cart.quantity>1:       
        cart.quantity-=1    
        cart.totalprice=cart.quantity*cart.product_name.price                    
        cart.save()      
    return redirect('/cart')
def cart(request):  
    cart_items=Cart.objects.filter(user=request.user)  
    total_price=sum(item.totalprice for item in cart_items)  
    return render(request,'html/cart.html',{'cart_items':cart_items,'total_price':total_price})  
def remove_from_cart(request,cart_id):  
    cart=get_object_or_404(Cart,id=cart_id,user=request.user)        
    cart.delete()  
    return redirect("/cart")  


from django.urls import reverse   
from django.http import HttpResponse     
from django.views.decorators.csrf import csrf_exempt    
from paypalrestsdk import Payment 
from .forms import ShippingAddressForm           
from .models import Order,Cart                                   

@csrf_exempt   
def execute_payment(request):  
    payment_id=request.GET.get('paymentId')  
    payer_id=request.GET.get('payerID')  
    payment=Payment.find(payment_id) 
    if payment.execute({"payer_id":payer_id}):   
        return render(request,'order_success.html') 
    else:  
        return HttpResponse('Error in executing payment')  
    
def cancel_payment(request):  
    return render(request,'payment_cancel.html') 

def checkout(request):  
    if request.method=='POST': 
        shipping_address_form=ShippingAddressForm(request.POST)  
        if shipping_address_form.is_valid():  
            shipping_address=shipping_address_form.save(commit=False)  
            shipping_address.user=request.user    
            shipping_address.save() 
            order=Order(user=request.user,shipping_address=shipping_address)  
            cart_items=Cart.objects.filter(user=request.user,order__isnull=True)          
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)      
            order.save()   
            for cart_item in cart_items:   
                cart_item.order=order  
                cart_item.save()   
                
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)                           
            order.save() 
            payment_data={ 
                          "intent":"sale",
                          "payer":{
                            "payment_method":"paypal",  
                          } , 
                          "redirect_urls":{ 
                              "return_url":request.build_absolute_uri(reverse('execute_payment')),
                              "cancel_url":request.build_absolute_uri(reverse('cancel_payment')), 
                              },  
                          "transactions":[{
                              "item_list":{ 
                                  "items":[{ 
                                      "name": item.product_name.name,      
                                      "sku":"item",    
                                      "price":str(item.product_name.price), 
                                      "currency":"USD",     
                                      "quantity":item.quantity, 
                              }for item in cart_items   ],  
                              },    
                              "amount":{
                                  "total":str(order.total_price),  
                                  "currency":"USD",    
                              },  
                              "description":"Order payment"
                            }],  
                          
            }    
            payment=Payment(payment_data)  
            if payment.create():  
                order.payment_id=payment.id    
                order.save()    
                return_url=[link.href for link in payment.link if link.method== "REDIRECT"][0]                 
                return redirect(return_url)    
            else:    
                return HttpResponse(f'Error in creating payment:{payment.error}')    
            
    else:     
        shipping_address_form=ShippingAddressForm()  
        
    return render(request,'html/checkout.html',{'shipping_address_form':shipping_address_form})     
