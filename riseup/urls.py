from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name="riseupHome"),
    path('signup/', views.signup, name="riseupSignup"),
    path('login/', views.userLogin, name="riseupLogin"),
    path('logout/', views.userLogout, name="riseupLogout"),
    path('tracker/', views.tracker, name="riseupTracker"),
    path('profile/', views.profile, name="riseupProfile"),
    path('request/', views.request, name="request"),
    path('startup/<int:myid>/', views.startup, name="riseupStartup"),
]