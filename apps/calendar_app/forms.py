from django.forms import ModelForm, DateInput
from .models import Event

# New calender event form
class EventForm(ModelForm):
  # input_formats to parse HTML5 datetime-local input to datetime field
  input_formats = ['%Y-%m-%dT%H:%M']
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['title', 'description', 'start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)