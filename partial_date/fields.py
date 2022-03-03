# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import re
import six

from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _

# I have to figure out the regex for this.  It's already kind of scary. Use 'T' to start any timepart
# additional parts are , YYYY-MM-DDTHH, YYYY-MM-DDTHH:mm
partial_date_re = re.compile(
    r"^(?P<year>\d{4})(?:-(?P<month>\d{1,2}))?(?:-(?P<day>\d{1,2}))?$"
)


class PartialDateTime(object):
    YEAR = 0
    MONTH = 1
    DAY = 2
    HOUR = 3
    MINUTE = 4

    _date = None
    _precision = None

    DATE_FORMATS = {YEAR: "%Y", MONTH: "%Y-%m", DAY: "%Y-%m-%d", HOUR: "%Y-%m-%d %H:00", MINUTE: "%Y-%m-%d %H:%M"}

    def __init__(self, date, precision=DAY):
        if isinstance(date, six.text_type):
            date, precision = PartialDateTme.parseDate(date)

        self.date = date
        self.precision = precision

    def __repr__(self):
        return (
            ""
            if not self._date
            else self._date.strftime(self.DATE_FORMATS[self._precision])
        )

    def format(self, precision_year=None, precision_month=None, precision_day=None, precision_hour=None, precision_minute=None):
        if self.precisionYear():
            format = precision_year
        elif self.precisionMonth():
            format = precision_month
        elif self.precisionDay():
            format = precision_day
        elif self.precisionHour():
            format = precision_hour            
        else:
            format = precision_minute
        return "" if not self._date else self._date.strftime(format)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime.date):
            raise exceptions.ValidationError(
                _("%(value)s is not datetime.date instance"), params={"value": value}
            )
        self._date = value

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        # TODO figure this out
        self._precision = (
            value if value in (self.YEAR, self.MONTH, self.DAY) else self.DAY
        )
        if self._precision == self.MONTH:
            self._date.replace(day=1)
        if self._precision == self.YEAR:
            self._date.replace(month=1, day=1)

    def precisionYear(self):
        return self.precision == self.YEAR

    def precisionMonth(self):
        return self.precision == self.MONTH

    def precisionDay(self):
        return self.precision == self.DAY
    
    def precisionHour(self):
        return self.precision == self.HOUR
    
    def precisionMinute(self):
        return self.precision == self.MINUTE    

    @staticmethod
    def parseDateTime(value):
        """
        Returns a tuple (datetime.date, precision) from a string formatted as YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDTHH, YYYY-MM-DDTHH:mm.
        """
        # TOOD this class
        match = partial_date_re.match(value)

        try:
            match_dict = match.groupdict()
            kw = {k: int(v) if v else 1 for k, v in six.iteritems(match_dict)}

            precision = (
                PartialDate.DAY
                if match_dict["day"]
                else PartialDate.MONTH
                if match_dict["month"]
                else PartialDate.YEAR
            )
            return (datetime.date(**kw), precision)
        except (AttributeError, ValueError):
            raise exceptions.ValidationError(
                _("'%(value)s' is not a valid date string (YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDTHH, YYYY-MM-DDTHH:mm)"),
                params={"value": value},
            )

    def __eq__(self, other):
        if isinstance(other, PartialDate):
            return self.date == other.date and self.precision == other.precision
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PartialDate):
            return self.__ge__(other) and not self.__eq__(other)
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PartialDate):
            return self.date >= other.date and self.precision >= other.precision
        else:
            return NotImplemented


class PartialDateTimeField(models.Field):
    """
    A django model field for storing partial datetimes.
    Accepts None, a partial_date.PartialDate object,
    or a formatted string such as YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDTHH, YYYY-MM-DDTHH:mm.
    In the database it saves the date in a column of type DateTimeField
    and uses the seconds to save the level of precision.
    """

    def get_internal_type(self):
        return "DateTimeField"

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return value
        return PartialDateTime(value.date(), value.second)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, PartialDateTime):
            return value

        if isinstance(value, six.text_type):
            return PartialDateTime(value)

        raise exceptions.ValidationError(
            _(
                "'%(name)s' value must be a PartialDateTime instance, "
                "a valid partial datetime string (YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DD HH(:00???), YYYY-MM-DD HH:mm) "
                "or None, not '%(value)s'"
            ),
            params={"name": self.name, "value": value},
        )

    # TODO figure out this part
    def get_prep_value(self, value):
        if value in (None, ""):
            return None
        partial_datetime = self.to_python(value)
        date = partial_datetime.date
        return datetime.datetime(
            date.year, date.month, date.day, second=partial_date.precision
        )
