
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('event_App/',include('event_App.urls')),
    path('admin_mng/',include('admin_mng.urls')),
    path('manager_app/',include('manager_app.urls')),
    # path('',include('admin_mng.urls')),
    # path('admin_mng/',include('admin_mng.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
