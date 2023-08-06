__version__ = "0.1.1"

import re
import datetime

from .six import string_types


TIME_PERIOD_REGEX = (
    r"^"
    r"((?P<days>\d+)d)?"
    r"((?P<hours>\d+)h)?"
    r"((?P<minutes>\d+)m)?"
    r"((?P<seconds>\d+)s)?"
    r"$"
)


def to_timedelta(time_period):  # type (str) -> datetime.timedelta
    """
    Return the timedelta object derived from the string representation of a time period.

    >>> import ptimedelta as ptd
    >>> ptd.to_timedelta("10m")
    datetime.timedelta(seconds=600)
    >>> ptd.to_timedelta("43m")
    datetime.timedelta(seconds=2580)
    >>> ptd.to_timedelta("1m27s")
    datetime.timedelta(seconds=87)
    >>> ptd.to_timedelta("65s")
    datetime.timedelta(seconds=65)
    >>> ptd.to_timedelta("3h2m")
    datetime.timedelta(seconds=10920)
    >>> ptd.to_timedelta("2d4s")
    datetime.timedelta(days=2, seconds=4)

    For Python2.7 unicode strings are also supported:

    >>> ptd.to_timedelta(u"3m2s")
    datetime.timedelta(seconds=182)
    """
    if not isinstance(time_period, string_types):
        raise TypeError(
            "Valid data type is string but %s is given." % type(time_period).__name__
        )

    if not time_period:
        raise ValueError("Empty string is an invalid time period.")

    matched = re.match(TIME_PERIOD_REGEX, time_period)

    if matched:
        return datetime.timedelta(
            **{
                key: int(value)
                for key, value in matched.groupdict().items()
                if value is not None
            }
        )

    raise ValueError("Given string `%s` is an invalid time period." % time_period)


def to_seconds(time_period, as_int=False):  # type (str, bool) -> Union[int, float]
    """
    Convert a time period represented by a string to the number of seconds.

    :param time_period: Time period.
    :type time_period: str
    :param as_int: If equals to `True` the return value is casted to the integer.
    :type as_int: bool

    Examples:
    >>> import ptimedelta as ptd
    >>> ptd.to_seconds("56m29s")
    3389.0
    >>> ptd.to_seconds("0s", as_int=True)
    0
    """
    seconds = to_timedelta(time_period).total_seconds()

    if as_int:
        return int(seconds)
    else:
        return seconds


def _doctest():  # type () -> None
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    _doctest()
