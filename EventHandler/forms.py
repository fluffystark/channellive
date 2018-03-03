from django.forms import ModelForm
from .models import Event


class EventForm (ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'category', 'start_date', 'end_date']
