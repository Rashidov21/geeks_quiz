from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('categories/', views.category_view, name='categories'),
    path('quiz/<int:category_id>/', views.quiz_view, name='quiz'),
    path('result/<int:result_id>/', views.result_view, name='result'),
]
