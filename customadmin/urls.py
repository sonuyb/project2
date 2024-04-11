from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from. import views


urlpatterns = [
    path('dash/',views.admin_dash,name='dash'),
    path('products/',views.products,name='products'),
    path('add-products/',views.add_products,name='add_products'),
    path('view-products/',views.view_products,name='view_products'),
    path('edit/<pk>',views.edit,name='edit'),
    path('delete/<pk>',views.delete,name='delete'),
    path('allorders/',views.view_all_orders,name='allorders'),
    path('update/<int:order_id>',views.update_order_status,name='update')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)