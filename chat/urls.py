from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'rooms', views.ChatRoomViewSet, basename='chatroom')

urlpatterns = [
 
    
    # # User endpoints
    # path('users/', views.get_user, name='get_users'),
    # path('users/me/', views.get_current_user, name='current_user'),
    # path('users/search/', views.search_users, name='search_users'),
    
    # Chat room endpoints (automatically includes CRUD)
    path('', include(router.urls)),
]