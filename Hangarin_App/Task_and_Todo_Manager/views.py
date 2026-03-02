from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Task_and_Todo_Manager.models import Task
from Task_and_Todo_Manager.forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q, F

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.count()

        completed = Task.objects.filter(
            status="Completed"
        ).count()

        context["completed"] = completed

        In_Progress = Task.objects.filter(
            status="In Progress "
        ).count()

        context["In_Progress"] = In_Progress

        Pending = Task.objects.filter(
            status="Pending"
        ).count()

        context["Pending"] = Pending

        completed_onTime = Task.objects.filter(
            status="Completed",
            updated_at__lte=F('deadline')
        ).count()

        completed_late = Task.objects.filter(
            status="Completed",
            updated_at__gt=F('deadline')
        ).count()

        if completed > 0:
            completion_rate = int((completed/context["total_tasks"]) * 100)
        else:
            completion_rate = 0

        if completed_onTime:
            compliancy_rate = int((completed_onTime/completed) * 100)
        else:
            compliancy_rate = 0

        if completed_late:
            deliquency_rate = int((completed_late/completed) * 100)
        else:
            deliquency_rate = 0


        context["Completion_rate"] = f"{completion_rate}%"
        context["Compliancy_rate"] = f"{compliancy_rate}%"
        context["Deliquency_rate"] = f"{deliquency_rate}%"
        
        return context

class TaskView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskList.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        
        query = self.request.GET.get('q')
        p_val = self.request.GET.get('priority')
        c_val = self.request.GET.get('category')
        s_val = self.request.GET.get('status')

        if query:
            qs = qs.filter(title__icontains=query)

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