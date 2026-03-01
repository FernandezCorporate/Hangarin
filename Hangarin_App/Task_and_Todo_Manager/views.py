from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Task_and_Todo_Manager.models import Task
from Task_and_Todo_Manager.forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

class TaskView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskList.html'
    paginate_by = 5

    def get_queryset(self):
        # 1. Start with the full list
        qs = super().get_queryset()
        
        # 2. Get values from URL
        query = self.request.GET.get('q')
        p_val = self.request.GET.get('priority')
        c_val = self.request.GET.get('category')
        s_val = self.request.GET.get('status')

        # 3. Apply Search (Only if query exists)
        if query:
            qs = qs.filter(title__icontains=query)

        # 4. Apply Filters (Only if they are not "All" and not None)
        if p_val and p_val != "All":
            qs = qs.filter(priority__name__iexact=p_val)

        if c_val and c_val != "All":
            qs = qs.filter(category__name__iexact=c_val)

        if s_val and s_val != "All":
            qs = qs.filter(status__iexact=s_val)

        return qs
    

    
    def get_ordering(self):
        allowed = ["priority", "category__name", "status", "deadline"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "status"

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

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')