from django.urls import path
from . import views

urlpatterns = [
    path('floating-button/', views.floating_button_view, name='floating_button_view'),
    path('bingo.html/', views.bingo, name='bingo'),
    path('towers-of-hanoi/', views.towers_of_hanoi, name='towersofhanoi'),
    path('snake/', views.snake, name='snake'),
    path('hangman/', views.hangman, name='hangman'),
    path('sudoku/', views.sudoku, name='sudoku'),
    path('Match-Cards/', views.memory, name='memory'),
    path('Quiz-Time/', views.quiz, name='quiz'),
    path('Word-Guess/', views.guess, name='guess'),
    path('chess/', views.chess, name='chess'),
    path('mathsprint', views.mathsprint, name='mathsprint'),
]
