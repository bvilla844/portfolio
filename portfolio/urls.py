from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('base.urls')),    
    path('catrina/', include(('productos.urls', 'products'), namespace='products')),
    path('to_dolist/', include('to_dolist.urls')),
    path('slot/', include('games.slot.urls')),
    path('battleship/', include('games.battleship.urls')),

]
# Esto permite servir archivos media (solo con DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)