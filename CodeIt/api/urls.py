from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('questions/', views.getQuestions),
    path('question/<str:pk>/', views.getQuestion),
]
