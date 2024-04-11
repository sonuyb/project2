from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from. import views


urlpatterns = [
    path('cart/', views.show_cart, name='cart'),
    path('add-cart/', views.add_to_cart, name='add_cart'),
    path('remove-item/<int:pk>/', views.remove_item, name='remove_item'),
    path('payment/<int:pk>', views.make_payment, name='payment'),
    path('orders/', views.view_orders, name='orders'),
    path('place_order/', views.place_order, name='place_orders'),
    path('view_order_details/<int:pk>', views.view_order_details, name='order_details'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)