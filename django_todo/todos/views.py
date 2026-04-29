from django.http import Http404
from django.shortcuts import render, redirect
from . import db


def index(request):
    return render(request, 'todos/index.html', {'todos': db.list_todos()})


def add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            db.create_todo(title)
        return redirect('index')
    return render(request, 'todos/add.html')


def toggle(request, pk):
    if db.get_todo(pk) is None:
        raise Http404
    db.toggle_completed(pk)
    return redirect('index')


def edit(request, pk):
    todo = db.get_todo(pk)
    if todo is None:
        raise Http404
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            db.update_title(pk, title)
        return redirect('index')
    return render(request, 'todos/edit.html', {'todo': todo})


def delete(request, pk):
    if db.get_todo(pk) is None:
        raise Http404
    db.delete_todo(pk)
    return redirect('index')
