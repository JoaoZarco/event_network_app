from django.test import SimpleTestCase
from django.urls import reverse, resolve
from event.views import (
    EventDraftView, 
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDetailedView
)

class TestEventUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('event-home')
        self.assertEquals(resolve(url).func.view_class, EventListView)

    def test_draft_url_is_resolved(self):
        url = reverse('event-drafts')
        self.assertEquals(resolve(url).func.view_class, EventDraftView)

    def test_detail_url_is_resolved(self):
        url = reverse('event-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, EventDetailedView)

    def test_create_url_is_resolved(self):
        url = reverse('event-form')
        self.assertEquals(resolve(url).func.view_class, EventCreateView)

    def test_update_url_is_resolved(self):
        url = reverse('event-update', args=[1])
        self.assertEquals(resolve(url).func.view_class, EventUpdateView)