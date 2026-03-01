from django.db import models
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True

class Category(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Priority(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name
    
class Task(BaseModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    deadline = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50,
        choices=[
        ("Pending", "Pending"),
        ("In Progress ", "In Progress"),
        ("Completed", "Completed"),
        ],
        default="Pending"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    status = models.CharField(
        max_length=50,
        choices=[
        ("Pending", "Pending"),
        ("In Progress ", "In Progress"),
        ("Completed", "Completed"),
        ],
        default="pending"
    )

    def __str__(self):
        return self.title
