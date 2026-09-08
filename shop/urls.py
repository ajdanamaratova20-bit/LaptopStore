from django.urls import path
from . import views

urlpatterns = [
    path('', views.laptop_list, name='laptop_list'),
    path('laptop/<int:pk>/', views.laptop_detail, name='laptop_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:laptop_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:laptop_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/add/<int:laptop_id>/', views.favorite_add, name='favorite_add'),
    path('favorite/remove/<int:laptop_id>/', views.favorite_remove, name='favorite_remove'),
]

