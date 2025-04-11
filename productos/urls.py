from django.contrib import admin
from django.urls import path
from productos import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'products'


urlpatterns = [
    path('sell/', views.sell, name='sell'),
    
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.singout, name='signout'),
    
    path('home', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('total_orders/', views.total_orders, name='total_orders'),
    path('orders/', views.orders, name='orders'),
    path('buy_product/<int:product_id>', views.buy_product, name='buy_product'),
    path('order_product/<int:product_id>/', views.order_product, name='order_product'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    path('create_product/', views.create_product, name='create_product'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('product_delete/<int:product_id>', views.delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)