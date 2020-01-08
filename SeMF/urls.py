
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('semf/', admin.site.urls),
    path('',include('RBAC.urls')),
    re_path(r'^$', views.log_in, name='logins'),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
    
handler404 = views.page_not_found
handler500 = views.page_error
handler403 = views.permission_denied