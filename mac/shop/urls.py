from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.login,name='index'),
    path('home/', views.index),
    path('logout/', views.logout),
    path('about/', views.about,name='AboutUs'),
    path('contact/', views.contact,name='ContactUs'),
    path('tracker/', views.tracker,name='TrackingStatus'),
    path('search/<str:ll>/', views.search,name='Search'),
    path('products/<int:myid>/', views.productview,name='ProductView'),
    path('checkout/', views.checkout,name='Checkout'),

]