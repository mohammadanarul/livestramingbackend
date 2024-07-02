from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# livetreamingBackend/urls.py
# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apihandle.views import MatchViewSet

router = DefaultRouter()
router.register(r'matches', MatchViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)