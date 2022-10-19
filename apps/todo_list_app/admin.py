from django.contrib import admin
from .models import ToDoItem, ToDoList

# Register models for the admin site
admin.site.register(ToDoItem)
admin.site.register(ToDoList)