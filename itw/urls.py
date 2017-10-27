
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from medicare.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'blog', include('blog.urls')),
    url(r'getblood/$', get_blood),
    url(r'^ambulancedetails/$', ambulancedetails),
    url(r'^contactus/$', contactus),
    url(r'takeapptmnt', takeapptmnt),
    url(r'apptmnttaken', apptmntdone),
    url(r'show_appointments', show_appointments), 
]

urlpatterns += [
    url(r'^medicare/', include('medicare.urls')),
]
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/medicare/', permanent=True)),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_rot = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
