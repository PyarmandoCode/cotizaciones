
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cotizacion.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Servir archivos de medios durante el desarrollo (no recomendado para producción)


handler404 = 'cotizacion.views.handler404'
handler500 = 'cotizacion.views.handler500'