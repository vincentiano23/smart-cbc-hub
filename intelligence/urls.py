from django.urls import path
from .views import generate_lesson_view

urlpatterns = [
    path('generate/', generate_lesson_view, name='generate_lesson'),
]