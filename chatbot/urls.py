from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('api/csrf_token/', views.get_csrf_token, name='get_csrf_token')
]
