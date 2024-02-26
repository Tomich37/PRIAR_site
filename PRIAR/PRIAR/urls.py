from django.urls import path
from priar_site import views

urlpatterns = [
    path('', views.index),
]
