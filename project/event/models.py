from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .validators import validate_date_today_or_after
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Event(models.Model):

    PUBLIC = 'PUB'
    PRIVATE = 'PRI'
    DRAFT = 'D'

    State = [
        (DRAFT, _('Draft')),
        (PUBLIC, _('Public')),
        (PRIVATE, _('Private')),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField(validators=[validate_date_today_or_after])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=3,
        choices=State,
        default=State[0][0]
    )

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.pk:
            update_state = self.state
            current_state = self.__class__.objects.get(pk=self.pk).state
            if current_state == Event.PRIVATE or current_state == Event.PUBLIC:
                if update_state == Event.DRAFT:
                    raise ValidationError(
                        _('Cannot update Event back to Draft'))


class Subscription(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'event']]
