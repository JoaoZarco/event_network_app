
from django.test import TestCase
from event.models import Event
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class TestModels(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create user
        User = get_user_model()
        cls.user = User.objects.create_user(
            'temporary3', 'temporary@gmail.com', 'temporary')

        return super().setUpClass()

    def test_create_event(self):

        event = Event(
            title='title',
            description='description',
            date=datetime.datetime.now().date(),
            state='PUB',
            author_id=self.user.id
        )

        try:
            event.full_clean()
            event.save()
            pass
        except ValidationError as e:
            self.fail('raised validation error')

    def test_create_event_with_date_before_today_fails(self):

        event = Event(
            title='title',
            description='description',
            date=datetime.date(2021, 5, 28),
            state='D'
        )

        try:
            event.full_clean()
            self.fail('did not raise validation error')
        except ValidationError as e:
            self.assertTrue('date' in e.message_dict)

    def test_update_published_event_state_to_draft_fails(self):

        event = Event.objects.create(
            title='title',
            description='description',
            date=datetime.datetime.now().date(),
            state='PUB',
            author_id=self.user.id
        )

        # update state
        event.state = 'D'

        try:
            event.full_clean()
            self.fail('did not raise validation error')
        except ValidationError as e:
            self.assertTrue('__all__' in e.message_dict)
