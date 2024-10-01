
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('events/', include('events.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
