# """
# URL configuration for chatapplication project.

# It exposes the URLconf as a module-level variable named ``urlpatterns``.

# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/topics/urls/
# """

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('auth/', include('accounts.urls')),
#     path('', include('chat.urls')),
# ]




"""
URL configuration for chatapplication project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/auth/', include('accounts.urls')),
    path('api/chat/', include('chat.urls')),
]