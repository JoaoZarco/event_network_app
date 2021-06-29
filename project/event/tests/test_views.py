
from django.test import TestCase, Client
from django.urls import reverse
from event.models import Event, Subscription
from django.contrib.auth import get_user_model

import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        # setup urls
        cls.drafts_url = reverse('event-drafts')
        # Create user
        User = get_user_model()
        cls.user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')

        cls.simple_event_data = {
            'title': 'title1',
            'description': 'description1',
            'date': datetime.datetime.now().date(),
            'author': cls.user
        }

        return super().setUpClass()

    def create_logged_off_client(self) -> Client:
        return Client()

    def create_logged_on_client(self) -> Client:
        client = Client()
        client.login(username='temporary', password='temporary')
        return client

    def create_simple_event(self, state) -> Event:
        return Event.objects.create(
            title=self.simple_event_data['title'],
            description=self.simple_event_data['description'],
            date=self.simple_event_data['date'],
            state=state,
            author=self.user
        )

    def create_simple_draft_event(self) -> Event:
        return self.create_simple_event('D')

    def create_simple_public_event(self) -> Event:
        return self.create_simple_event('PUB')

    def create_simple_private_event(self) -> Event:
        return self.create_simple_event('PRI')

    def test_event_list(self):
        logged_off_client = self.create_logged_off_client()
        list_url = reverse('event-home')

        response = logged_off_client.get(list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/home.html')

    def test_event_drafts_logged_off(self):
        logged_off_client = self.create_logged_off_client()

        response = logged_off_client.get(self.drafts_url)
        self.assertEquals(response.status_code, 302)

    def test_event_drafts_logged_on(self):
        logged_on_client = self.create_logged_on_client()

        response = logged_on_client.get(self.drafts_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/drafts.html')

    def test_public_event_details(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_public_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_off_client.get(details_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')

    def test_private_event_details_logged_off(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_private_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_off_client.get(details_url)

        self.assertEquals(response.status_code, 302)

    def test_draft_event_details_logged_off(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_draft_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_off_client.get(details_url)

        self.assertEquals(response.status_code, 403)

    def test_private_event_details_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_private_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_on_client.get(details_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')

    def test_draft_event_details_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_draft_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_on_client.get(details_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')

    def test_create_event_logged_off(self):
        create_url = reverse('event-form')

        response = self.create_logged_off_client().post(create_url)

        self.assertEquals(response.status_code, 302)

    def test_create_event_logged_on(self):
        create_url = reverse('event-form')
        logged_on_client = self.create_logged_on_client()
        title = self.simple_event_data['title']
        description = self.simple_event_data['description']
        date = self.simple_event_data['date']
        state = 'PUB'

        response = logged_on_client.post(create_url, {
            'title': title,
            'description': description,
            'date': date,
            'state': state
        })
        event = Event.objects.get(id=1)
        author_id = self.simple_event_data['author'].id

        self.assertEquals(response.status_code, 302)
        self.assertEquals(event.title, title)
        self.assertEquals(event.description, description)
        self.assertEquals(event.date, date)
        self.assertEquals(event.state, state)
        self.assertEquals(event.author_id, author_id)

    def test_draft_event_details_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_draft_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_on_client.get(details_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')

    def test_create_subscription_logged_off(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_public_event()
        details_url = reverse('event-detail', args=[event.id])

        response = logged_off_client.post(details_url)

        self.assertEquals(response.status_code, 302)

    def test_create_subscription_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_private_event()
        details_url = reverse('event-detail', args=[event.id])
        comment = 'comment1'
        event_id = event.id

        response = logged_on_client.post(details_url, {
            'event_id': event.id,
            'comment': comment
        })
        subscription = Subscription.objects.get(id=1)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(subscription.comment, comment)

    def test_create_subscription_with_same_event_and_user_fails_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_private_event()
        details_url = reverse('event-detail', args=[event.id])
        comment = 'comment1'
        event_id = event.id

        logged_on_client.post(details_url, {
            'event_id': event.id,
            'comment': comment
        })

        try:
            logged_on_client.post(details_url, {
                'event_id': event.id,
                'comment': comment
            })
            self.fail('IntegrityError not raised')
        except IntegrityError:
            pass

    def test_get_update_event_page_logged_off(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_public_event()
        update_url = reverse('event-update', args=[event.id])

        response = logged_off_client.get(update_url)

        self.assertEquals(response.status_code, 302)

    def test_update_event_logged_off(self):
        logged_off_client = self.create_logged_off_client()
        event = self.create_simple_public_event()
        update_url = reverse('event-update', args=[event.id])

        response = logged_off_client.post(update_url)

        self.assertEquals(response.status_code, 302)

    def test_get_update_event_page_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_public_event()
        update_url = reverse('event-update', args=[event.id])

        response = logged_on_client.get(update_url)

        self.assertEquals(response.status_code, 200)

    def test_update_owned_event_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        event = self.create_simple_public_event()
        event_id = event.id
        update_url = reverse('event-update', args=[event_id])
        title = 'title_updated'
        description = 'description_updated'
        date = datetime.datetime.now().date()

        response = logged_on_client.post(update_url, {
            'title': title,
            'description': description,
            'date': date,
            'state': 'PRI'
        })

        updated_event = Event.objects.get(id=event_id)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(updated_event.title, title)
        self.assertEquals(updated_event.description, description)
        self.assertEquals(updated_event.date, date)
        self.assertEquals(updated_event.state, 'PRI')

    def test_update_non_owned_event_logged_on(self):
        logged_on_client = self.create_logged_on_client()
        # Create second user
        user = get_user_model().objects.create_user(
            'temporary2', 'temporary2@gmail.com', 'temporary2')
        # Use secondd user to create event
        event = Event.objects.create(
            title='title1',
            description='description1',
            date=datetime.datetime.now().date(),
            state='P',
            author=user
        )
        # update attributes
        event_id = event.id
        title = 'title_updated'
        description = 'description_updated'
        date = datetime.datetime.now().date()
        update_url = reverse('event-update', args=[event_id])

        # Try to update with main user
        response = logged_on_client.post(update_url)

        self.assertEquals(response.status_code, 403)

