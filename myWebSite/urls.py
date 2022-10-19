from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.login_app.urls')),
    path('todo_list/', include('apps.todo_list_app.urls')),
    path('calendar/', include('apps.calendar_app.urls')),
    path('gallery/', include('apps.gallery_app.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)