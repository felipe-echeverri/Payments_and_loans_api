from django.contrib import admin
from django.urls import path, include
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

urlpatterns = [
    # Rutas para generar y referescar tokens de JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('admin/', admin.site.urls),
    path('api/', include('loans_and_paids.urls')),
    path('docs/', include_docs_urls(
        title='Api Documentation',
        permission_classes=[AllowAny], # Permite el acceso sin autenticación
        )),
]
