from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", include("polls.urls")),
    path("vauth/", include("vauth.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += [(path('__debug__/', include("debug_toolbar.urls")))]
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)