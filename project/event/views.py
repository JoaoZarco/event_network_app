from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View
)
from .models import Event, Subscription
from .forms import CreateSubscriptionForm, EventForm

import datetime
from django.urls import reverse


class EventDraftView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/drafts.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user

        # query drafts associated with the author
        events = Event.objects.filter(
            Q(state=Event.DRAFT) &
            Q(author_id=user.id))

        return events


class EventListView(ListView):
    model = Event
    template_name = 'event/home.html'
    context_object_name = 'events'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # if user is authenticated query public and private Events
            events = Event.objects.filter(
                Q(state=Event.PUBLIC) |
                Q(state=Event.PRIVATE)).order_by('-date')
        else:
            # if not query public events only
            events = Event.objects.filter(state=Event.PUBLIC)

        return events


class EventDetailedView(UserPassesTestMixin, View):
    model = Event

    def get_event(self, pk):
        return get_object_or_404(Event, pk=pk)

    def is_user_author(self, event, user):
        return event.author_id == user.id

    def is_subscribable(self, event, is_subscribed):
        # if subscribed cannot subscribe again
        if is_subscribed:
            return False
        # Not subscribable if event is a draft
        if event.state == Event.DRAFT:
            return False
        # Not subscribable if already Subscribable
        return True

    def is_subscribed(self, event, user):
        return Subscription.objects.filter(
            Q(user_id=user.id) &
            Q(event_id=event.id)
        ).exists()

    def check_access(self, event, user):
        response = None
        # if the Event is private only authenticated users can see it
        if event.state == Event.PRIVATE:
            if(not user.is_authenticated):
                response = redirect('login')

        # if the Event is a Draft only the author can see it
        if event.state == Event.DRAFT:
            if event.author_id != user.id:
                response = HttpResponseForbidden()

        return response

    def get(self, request, *args, **kwargs):
        form = CreateSubscriptionForm()

        event = self.get_event(kwargs['pk'])
        user = request.user

        check_access_response = self.check_access(event, user)
        if check_access_response != None:
            return check_access_response

        is_subscribed = self.is_subscribed(event, user)
        is_subscribable = self.is_subscribable(event, is_subscribed)
        is_editable = self.is_user_author(event, user)

        context = {
            'event': event,
            'form': form,
            'title': event.title,
            'is_editable': is_editable,
            'is_subscribable': is_subscribable,
            'is_subscribed': is_subscribed
        }

        return render(request, 'event/event_detail.html', context)

    def post(self, request, *args, **kwargs):
        # add event and user
        form = CreateSubscriptionForm(request.POST)
        event_id = self.request.POST.get('event_id')
        user = self.request.user
        form.instance.event_id = event_id
        form.instance.user_id = user.id

        # get event
        event = self.get_event(event_id)

        check_access_response = self.check_access(event, user)
        if check_access_response != None:
            return check_access_response

        if form.is_valid():
            form.save()
            data = form.cleaned_data
            messages.success(request, f'Subscribed to event successfully!')
            redirect_url = reverse('event-detail', args=[event.id])
            return redirect(redirect_url)

        return render(request, 'event/event_detail.html', {'form': form, 'event': event})

    def test_func(self) -> bool:
        method = self.request.method
        if method == 'GET':
            return True
        elif method == 'POST':
            return self.request.user.is_authenticated
        else:
            return True


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs['is_published'] = False
        return kwargs


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

    def get_form_kwargs(self):
        kwargs = super(EventUpdateView, self).get_form_kwargs()
        event = self.get_object()
        kwargs['is_published'] = True if (
            event.state == Event.PRIVATE or event.state == Event.PUBLIC) else False

        return kwargs
