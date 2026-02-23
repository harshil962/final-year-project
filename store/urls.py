from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="contact"),
    path("tracker/",views.tracker,name="TrakingStatus"),
    path('search/', views.search, name='search'),
    path("products/<int:id>", views.productView, name="productview"),
    path("checkout/",views.checkout,name="Checkout"),
    path("paymenthandler/", views.paymenthandler, name="PaymentHandler"),  
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_conditions, name='terms_conditions'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path("shipping-policy/", views.shipping_policy, name="shipping_policy"),  
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.my_orders, name="MyOrders"),   

]
