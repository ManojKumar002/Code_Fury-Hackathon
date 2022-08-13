from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name="riseupIndex"),
    path('startup/', views.startup, name="riseupStartup"),
]