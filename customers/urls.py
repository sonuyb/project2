from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from. import views


urlpatterns = [
    path('account/',views.create_account,name='account'),
    path('login/',views.customer_login,name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/',views.user_logout,name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)