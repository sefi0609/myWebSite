from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Calculate one week ahead  
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

# Todolist model - create a table of todolist object
class ToDoList(models.Model):
    # Each todolist has an owner (user) - each user can see only their todolists  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

# Todoitem model - create a table of todoitem object, Todolist is a foreign key
class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    is_completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("item-update", args=[str(self.todo_list.id), str(self.id)])

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]








        