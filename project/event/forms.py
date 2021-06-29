from django import forms
from .models import Subscription, Event
from django.utils.translation import gettext_lazy as _
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):
    def __init__(self, is_published, *args, **kwargs):

        super(EventForm, self).__init__(*args, **kwargs)

        if is_published == True:
            self.fields['state'].choices = [Event.State[1], Event.State[2]]

    class Meta:
        model = Event
        widgets = {
            'date': DateInput(attrs={
                'min': datetime.datetime.now().date()
            })
        }
        fields = [
            'title',
            'description',
            'state',
            'date'
        ]
        labels = {
            "title": _('Title'),
            "description": _('Description'),
            "state": _('State'),
            "date": _('Date')
        }


class CreateSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'comment'
        ]
        labels = {
            "comment": _('Comment')
        }
