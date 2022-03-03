django_partial_datetime
================

This is forked from django_partial_date and I am adding Hours and Minutes.  I am curious if this will allow me to
store instantaneous observations (recorded to the minute) and annual and monthly and daily statistics for those observations in a single table.
I'm guessing that querying is going to be key - because queries will all need to use the precision flag.

Even though I don't want to use it, I wonder if I should include seconds and store the precision in milliseconds location just to allow for the additional step???

Django custom model field for partial datetimes with the form YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DD HH, YYYY-MM-DD HH:mm

 * Works with DRF
 * Supports comparison operations
 * Supports Django 2.0 and Django 3.0 and Django 4.0

Usage
================

install the package

```bash
pip install django_partial_datetime
```


## partial_datetime.PartialDateTimeField

A django model field for storing partial dates. Accepts None, a partial_date.PartialDateTime object, or a formatted string such as YYYY, YYYY-MM, YYYY-MM-DD, , YYYY-MM-DD HH, , YYYY-MM-DD HH:mm. In the database it saves the date in a column of type DateTimeField and uses the seconds to save the level of precision.

## class partial_date.PartialDateTime

Object to represent the partial date times.

## Example

models.py
```python
from django.db import models
from partial_date import PartialDateTimeField

class TestModel(models.Model):
    some_partial_datetime = PartialDateTimeField()
```

```python
>>> from partial_datetime import PartialDateTime
>>> from core.models import TestModel
>>> obj = TestModel(some_partial_datetime="1995")
>>> obj.save()
>>> obj.some_partial_datetime
'1995'
>>> obj.some_partial_date = PartialDateTime("1995-09")
>>> obj.save()
>>> obj.some_partial_datetime
1995-09
>>>
```

```python
>>> from partial_date import PartialDateTime
>>> import datetime
>>> partial_date_instance = PartialDateTime(datetime.date(2012, 9, 21), precision=PartialDate.DAY)
>>> partial_date_instance
2012-09-21
>>> partial_date_instance.precisionYear()
False
>>> partial_date_instance.precisionMonth()
False
>>> partial_date_instance.precisionDay()
True
>>> partial_date_instance.precision == PartialDate.YEAR
False
>>> partial_date_instance.precision == PartialDate.MONTH
False
>>> partial_date_instance.precision == PartialDate.DAY
True
>>> partial_date_instance.precision = PartialDate.MONTH
>>> partial_date_instance
2012-09
>>> partial_date_instance = PartialDate("2015-11-01")
>>> partial_date_instance.date
datetime.date(2015, 11, 1)
```


```python
>>> from partial_date import PartialDate
>>> partial_date_instance = PartialDate("2015-11-01")
>>> partial_date_instance
2015-11-01
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y') # .format(precision_year, precision_month, precision_day)
'11/01/2015'
>>> partial_date_instance = PartialDate("2015-11")
>>> partial_date_instance
2015-11
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y')
'11/2015'
>>> partial_date_instance = PartialDate("2015")
>>> partial_date_instance
2015
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y')
'2015'
```

Thanks for their collaborations to
- lorinkoz
- howieweiner
- jghyllebert
