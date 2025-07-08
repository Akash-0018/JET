from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def floating_button_view(request):
    return render(request, 'floating_button_view.html')

@login_required
def bingo(request):
    return render(request, 'bingo.html')

@login_required
def towers_of_hanoi(request):
    return render(request, 'towersofhanoi.html')

@login_required
def snake(request):
    return render(request, 'snake.html')

@login_required
def hangman(request):
    return render(request, 'hangman.html')

@login_required
def sudoku(request):
    return render(request, 'sudoku.html')

@login_required
def memory(request):
    return render(request, 'memory.html')

@login_required
def quiz(request):
    return render(request, 'quiz.html')

@login_required
def guess(request):
    return render(request, 'guess.html')

@login_required
def chess(request):
    return render(request, 'chess.html')

@login_required
def mathsprint(request):
    return render(request, 'mathsprint.html')
