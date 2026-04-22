from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo


def index(request):
    todos = Todo.objects.all()
    return render(request, 'todos/index.html', {'todos': todos})


def add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Todo.objects.create(title=title)
        return redirect('index')
    return render(request, 'todos/add.html')


def toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')


def edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            todo.title = title
            todo.save()
        return redirect('index')
    return render(request, 'todos/edit.html', {'todo': todo})


def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('index')
