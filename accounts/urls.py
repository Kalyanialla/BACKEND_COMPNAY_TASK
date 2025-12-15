# from django.urls import path 
# from . import views


# urlpatterns=[
#     path("singup/",views.Signup),
#     path("login/",views.Login),
#     path('logout/',views.Logout),
#     path('get_user/',views.get_user),
# ]


from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.Signup, name='signup'),  # FIXED: spelling
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Users
    path('users/', views.get_users, name='get_users'),
    path('users/me/', views.get_current_user, name='current_user'),
]