from django.urls import path
from priar_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('create_user/', views.create_user, name='create_user'),
    path('success/', views.success, name='success'),
    path("login_view/", views.login_view, name='login_view'),
]
