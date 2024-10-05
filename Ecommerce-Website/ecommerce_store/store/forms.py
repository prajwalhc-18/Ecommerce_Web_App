from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User                              
class SignupForm(UserCreationForm):  
    first_name=forms.CharField(max_length=40) 
    last_name=forms.CharField(max_length=40)   
    email=forms.EmailField(max_length=40)  
    class Meta:  
        model=User   
        fields=UserCreationForm.Meta.fields+('first_name','last_name','email')  
        
class SearchForm(forms.Form):  
    q=forms.CharField(label='search',max_length=50)  
    
from django import forms  
from .models import ShippingAddress 
class ShippingAddressForm(forms.ModelForm):  
    class Meta:  
        model=ShippingAddress 
        fields=['address_line1','address_line2','city','state','zip_code']   