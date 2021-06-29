from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-home'),
    path('myDrafts', views.EventDraftView.as_view(), name='event-drafts'),
    path('event/<int:pk>', views.EventDetailedView.as_view(), name='event-detail'),
    path('event/new', views.EventCreateView.as_view(), name='event-form'),
    path('event/<int:pk>/update/',
         views.EventUpdateView.as_view(), name='event-update'),
]
