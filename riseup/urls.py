from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name="riseupHome"),
    path('signup/', views.signup, name="shopSignup"),
    path('login/', views.userLogin, name="shopLogin"),
    path('logout/', views.userLogout, name="shopLogout"),
    path('startup/<int:myid>/', views.startup, name="riseupStartup"),
]