from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="home"),
    path('stella/', views.stella, name="bot"),
    path('about/', views.about, name="about"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('process_message/', views.process_message, name='process_message'),
    path('upload/', views.uploaded, name="upload"),
    path('logout/', views.logout, name="logout")
]
