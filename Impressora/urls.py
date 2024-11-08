from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biblioteca/', include('Imprimir.urls')),
    path('', include('Imprimir.urls')),
]