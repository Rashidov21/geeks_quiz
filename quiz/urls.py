from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('category/', views.category_selection_view, name='category_selection'),
    path('quiz/start/', views.quiz_view, name='start_quiz'),
    path('quiz/question/<int:question_num>/', views.quiz_question_view, name='quiz_question'),
    path('quiz/question/<int:question_num>/save/', views.save_answer_view, name='save_answer'),
    path('quiz/submit/', views.submit_quiz_view, name='submit_quiz'),
]

