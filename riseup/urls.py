from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name="riseupHome"),
    path('signup/', views.signup, name="shopSignup"),
    path('login/', views.userLogin, name="shopLogin"),
    path('logout/', views.userLogout, name="shopLogout"),
    path('tracker/', views.tracker, name="shopTracker"),
    path('request/', views.request, name="request"),
    path('startup/<int:myid>/', views.startup, name="riseupStartup"),
]