"""
Default date functions
"""
import calendar

from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone, formats

from .registry import nlf_function


try:
    #: Django uses 0 for Sunday and 1 for Monday. `FIRST_DAY_OF_WEEK` holds
    #: a :mod:`calendar <python:calendar>` compatible value,
    #: i.e. 0 for Monday and 6 for Sunday.
    FIRST_DAY_OF_WEEK = (formats.get_format("FIRST_DAY_OF_WEEK") - 1) % 7
except ImproperlyConfigured:
    FIRST_DAY_OF_WEEK = 0


@nlf_function("startOfWeek")
def start_of_week(*args, **kwargs):  # pylint: disable=unused-argument
    """
    Determines the first day of the the current week based on l10n settings.
    Time is set to `00:00:00`.

    :returns: A datetime object set to 00:00 on the first day of the current week.
    :rtype: :class:`datetime <python:datetime.datetime>`
    """
    now = timezone.now()

    day = now.day - (now.weekday() - FIRST_DAY_OF_WEEK)
    # this calculation gives the next start of week when
    # Friday, Saturday or Sunday are the start of week
    if FIRST_DAY_OF_WEEK > 3:
        day -= 7

    month = now.month
    year = now.year
    if day < 1:
        # the start of week is in the previous month
        month -= 1
        if month == 0:
            # before January we have December
            year -= 1
            month = 12

        _, max_days = calendar.monthrange(year, month)
        day = max_days + day

    return now.replace(year=year, month=month, day=day, hour=0, minute=0, second=0, microsecond=0)


@nlf_function("startOfMonth")
def start_of_month(*args, **kwargs):  # pylint: disable=unused-argument
    """
    Determines the first day of the current month. Time is set to `00:00:00`.

    :returns: A datetime object set to 00:00 on the first day of the current month.
    :rtype: :class:`datetime <python:datetime.datetime>`
    """
    now = timezone.now()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


@nlf_function("startOfYear")
def start_of_year(*args, **kwargs):  # pylint: disable=unused-argument
    """
    Determines the first day of the current year. Time is set to `00:00:00`.

    :returns: A datetime object set to 00:00 on the first day of the current year.
    :rtype: :class:`datetime <python:datetime.datetime>`
    """
    now = timezone.now()
    return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
