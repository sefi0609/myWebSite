from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ToDoList, ToDoItem
from django.urls import reverse, reverse_lazy

# List view class
class ListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = 'todo_list_app/all_lists.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['object_list'] = context['object_list'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['object_list'] = context['object_list'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context

# Item view class
class ItemListView(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = 'todo_list_app/todo_list.html'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context

# Create list view
class ListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(ListCreate, self).get_context_data(**kwargs)
        context['title'] = 'Add a new list'
        return context
    # Make sure the user field in the model is the current user  
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ListCreate, self).form_valid(form)

# Create item view (inside each list)
class ItemCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date', 'is_completed']

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = 'Create a new item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])

# A view to update an item
class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date', 'is_completed']

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        context['title'] = 'Edit item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])

# Delete a list view
class ListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy('all_lists')

# Delete an item view
class ItemDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.kwargs['list_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context