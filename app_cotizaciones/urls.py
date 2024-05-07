
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cotizacion.urls'))
]


handler404 = 'cotizacion.views.handler404'
handler500 = 'cotizacion.views.handler500'