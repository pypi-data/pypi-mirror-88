
import time
import datetime as dt

from typing import Union

def is_weekend(d: Union[dt.datetime,dt.date]) -> bool:
    """Check if date ``d`` is a weekend.

    :param d: Date or datetime to check for weekend-ness
    """
    return d.weekday() >= 5

def is_weekday(d: Union[dt.datetime,dt.date]) -> bool:
    """Check if date ``d`` is a weekday.

    :param d: Date or datetime to check for weekday-ness
    """
    return not is_weekend(d)

def get_date(d: dt.datetime) -> dt.date:
    """Extract date object from datetime ``d``.

    :param d: Datetime to extract date from.
    """
    return d.date()

def get_time(d: dt.datetime) -> dt.time:
    """Extract time object from datetime ``d``.

    :param d: Datetime to extract time from.
    """
    return d.time()

def to_ordinal(d: Union[dt.datetime,dt.date]) -> int:
    """Converts a date object to an integer.

    Wraps ``dt.datetime.toordinal()``.

    "Return proleptic Gregorian ordinal.
    January 1 of year 1 is day 1."

    :param d: Datetime to convert to int
    """
    return d.toordinal()

def get_season(d: Union[dt.date,dt.datetime], as_string: bool = True,
    north: bool = True) -> Union[str,int]:
    """Get the season for date ``d``.

    *Season Table:*

    ======  ======  ===========  ==============
    North   South   Start Date   End Date
    ======  ======  ===========  ==============
    Winter 	Summer 	1 December 	 28/29 February
    Spring 	Autumn 	1 March 	 31 May
    Summer 	Winter 	1 June 	     31 August
    Autumn 	Spring 	1 September  30 November
    ======  ======  ===========  ==============

    :param d: Date used to extract season
    :param as_string: Return season name or as ordinal
    :param north: Northern hemisphere (or southern hemisphere)
    :return: ``d``'s season as a ``str`` or ``int``
    """
    if d.month == 12 or d.month < 3:
        if north:
            return "winter" if as_string else 3
        else:
            return "summer" if as_string else 1
    elif d.month < 6:
        if north:
            return "spring" if as_string else 0
        else:
            return "fall" if as_string else 2
    elif d.month < 9:
        if north:
            return "summer" if as_string else 1
        else:
            return "winter" if as_string else 3
    else:
        if north:
            return "fall" if as_string else 2
        else:
            return "sprint" if as_string else 0
