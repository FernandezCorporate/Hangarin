from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from Task_and_Todo_Manager.models import Task
from Task_and_Todo_Manager.forms import TaskForm
from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

class TaskView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskList.html'
    paginate_by = 5

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')