from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_date_today_or_after(value):
    if value < datetime.datetime.now().date():
        raise ValidationError(
            _("Selected Date for event should be today or after."))
    return value
