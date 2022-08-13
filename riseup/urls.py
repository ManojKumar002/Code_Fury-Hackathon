from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name="riseupIndex"),
    path('startup/<int:myid>/', views.startup, name="riseupStartup"),
]