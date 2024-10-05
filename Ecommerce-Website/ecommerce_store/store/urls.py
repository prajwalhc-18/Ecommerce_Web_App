
from django.urls import path,include
from . import views      
from django.contrib.auth.views import LoginView              
urlpatterns=[
    path("dashboard",views.dashboard,name="dashboard"),
    path("<int:id>",views.product_details,name="product_details"),  
    path("login",views.user_login,name="login"),     
    path('accounts/login/' ,LoginView.as_view(template_name="html/login.html"),name='login'),        
    path('logout',views.user_logout,name="logout") ,        

    path('search',views.SearchResultsView.as_view(),name="search_results"), 
    path("",views.signup,name="signup"),   
    path('add_to_cart/',views.add_to_cart,name="add_to_cart") ,     
    path("increment_cart/<int:cart_id>/",views.increment_cart, name="increment_cart"), 
    path('decrement_cart/<int:cart_id>/',views.decrement_cart,name="decrement_cart")  ,  
    path('cart/',views.cart,name="cart"),  
    path('remove_from_cart/<int:cart_id>/',views.remove_from_cart,name="remove_from_cart"),   
    path("checkout/",views.checkout,name="checkout"),  
    path("execute-payment/",views.execute_payment,name="execute_payment"), 
    path("cancel-payment/",views.cancel_payment,name="cancel_payment"),   
    
    ]  