from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from. import views


urlpatterns = [
    path('',views.index,name='home'),
    path('list-product',views.list_products,name='list_product'),
    path('product-detail/<int:pk>',views.product_details,name='product_details'),
    path('product-review/<int:pk>',views.product_review,name='product_review'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)