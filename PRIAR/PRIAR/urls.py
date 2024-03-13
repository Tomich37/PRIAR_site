from django.urls import path
from priar_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about),
    path('services', views.services),
    path('login', views.login)
]
