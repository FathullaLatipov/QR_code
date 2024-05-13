from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from qrapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('product_info/<int:pk>', views.product_info, name='product_info'),
    path('', views.generate_home, name='product_qr'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
