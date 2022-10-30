from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView
from django.utils.safestring import mark_safe
# Block unwanted access to views 
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
from django.contrib import messages
from django.urls import reverse_lazy

from .models import *
from .utils import Calendar
from .forms import EventForm

# Calendar view - uses the utils file
class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendar_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = new_event(self.request)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        return context

# Calculate the previous month for the calender view
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

# Calculate the next month for the calender view
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# Return today's day for the calender view
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, 1)
    return datetime.today()

# A view to create a new calender event
def new_event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    # Uses the forms file
    form = EventForm(request.POST or None, instance=instance)
    # Make sure the user field in the model is the current user   
    form.instance.user = request.user
    # Check for valid information 
    if request.POST and form.is_valid():
        if form.instance.start_time <= form.instance.end_time:
            form.save()
            return HttpResponseRedirect(reverse('calendar'))
        else:
            messages.info(request, "The start time can't be after the end time")
    return render(request, 'calendar_app/new_event.html', {'form': form})

# A class view to update an event
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'calendar_app/update_event.html'
    success_url = reverse_lazy('calendar')

    # Or you can use the function below
    #def get_success_url(self):
    #    return reverse('calendar')

    def get_context_data(self):
        context = super(EventUpdate, self).get_context_data()
        context['event_id'] = self.object.id
        return context

# A class view to delete an event
class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy('calendar')
