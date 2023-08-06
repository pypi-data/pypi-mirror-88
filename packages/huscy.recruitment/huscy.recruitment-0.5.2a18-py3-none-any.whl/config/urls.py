from django.contrib import admin
from django.urls import path, re_path, include

from huscy.recruitment.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
