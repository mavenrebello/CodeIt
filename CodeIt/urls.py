from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('question-page/<str:pk>/',views.questionPage, name='question-page'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('question-submit/', views.questionSubmit, name="question-submit"),
    path('delete-question/<str:pk>/', views.deleteQuestion, name='delete-question'),
    path('update-question/<str:pk>/', views.updateQuestion, name='update-question'),
    path('answer-submit/<str:pk>', views.answerSubmit, name="answer-submit"),
    path('comment-submit/<str:pk>', views.commentSubmit, name="comment-submit"),
    path('delete-answer/<str:pk>/', views.deleteAnswer, name='delete-answer'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('update-answer/<str:pk>/', views.updateAnswer, name='update-answer'),
    path('update-comment/<str:pk>/', views.updateComment, name='update-comment'),

]