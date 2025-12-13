from django.urls import path 
from . import views


urlpatterns=[
    path("singup/",views.Signup),
    path("login/",views.Login),
    path('logout/',views.Logout),
    path('get_user/',views.get_user),
]