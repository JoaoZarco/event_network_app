
from django.test import SimpleTestCase
from event.forms import EventForm, CreateSubscriptionForm
from django.contrib.auth.models import User
import datetime


class TestForms(SimpleTestCase):

    def test_create_event_form_valid_data(self):
        form = EventForm(data={
            'title': 'title1',
            'description': 'description1',
            'date': datetime.datetime.now().date(),
            'state': 'D',
            'author_id': 1
        }, is_published=False)

        self.assertTrue(form.is_valid())

    def test_create_event_form_no_data(self):
        form = EventForm(data={}, is_published=False)

        self.assertFalse(form.is_valid())

    def test_create_subscription_form_valid_data(self):
        form = CreateSubscriptionForm(data={
            'comment': 'comment1'
        })

        self.assertTrue(form.is_valid())

    def test_create_subscription_form_no_data(self):
        form = CreateSubscriptionForm(data={})

        self.assertFalse(form.is_valid())
